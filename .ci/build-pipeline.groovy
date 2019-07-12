def run_tests(stage_name, env_array, chunk_timeout) {
    return {
        def stage_slug = stage_name.replace('#', '').replace(' ', '-').toLowerCase()
        def checkout_dir = "${checkout_directory}-${stage_slug}"
        sh "cp -Rp $checkout_directory $checkout_dir"
        dir(checkout_dir) {
            withEnv(env_array) {
                stage(stage_name) {
                    stage('Create VM') {
                        retry(3) {
                            sh '''
                            t=$(shuf -i 30-90 -n 1); echo "Sleeping $t seconds"; sleep $t
                            bundle exec kitchen create $TEST_SUITE-$TEST_PLATFORM; echo "ExitCode: $?";
                            '''
                        }
                    }
                    try {
                        sshagent(credentials: ['jenkins-testing-ssh-key']) {
                            sh 'ssh-add ~/.ssh/kitchen.pem'
                            try {
                                timeout(time: chunk_timeout, unit: 'HOURS') {
                                    stage('Converge VM') {
                                        sh 'bundle exec kitchen converge $TEST_SUITE-$TEST_PLATFORM; echo "ExitCode: $?";'
                                    }
                                    stage('Run Tests') {
                                        withEnv(["DONT_DOWNLOAD_ARTEFACTS=1"]) {
                                            sh 'bundle exec kitchen verify $TEST_SUITE-$TEST_PLATFORM; echo "ExitCode: $?";'
                                        }
                                    }
                                }
                            } finally {
                                try {
                                    stage('Download Artefacts') {
                                        withEnv(["ONLY_DOWNLOAD_ARTEFACTS=1"]){
                                            sh '''
                                            bundle exec kitchen verify $TEST_SUITE-$TEST_PLATFORM || exit 0
                                            '''
                                        }
                                    }
                                    junit 'artifacts/xml-unittests-output/*.xml'
                                } finally {
                                    stage('Cleanup') {
                                        sh '''
                                        bundle exec kitchen destroy $TEST_SUITE-$TEST_PLATFORM; echo "ExitCode: $?";
                                        '''
                                    }
                                    stage('Upload Coverage') {
                                        retry(3) {
                                            timeout(time: 5, unit: 'MINUTES') {
                                                script {
                                                    withCredentials([[$class: 'StringBinding', credentialsId: 'codecov-upload-token-salt', variable: 'CODECOV_TOKEN']]) {
                                                      sh '''
                                                      if [ -n "${FORCE_FULL}" -a "${FORCE_FULL}" = "true" -a -f artifacts/coverage/coverage.xml ]; then
                                                          curl -L https://codecov.io/bash | /bin/sh -s -- -R $(pwd) -s artifacts/coverage/ -F "${CODECOV_FLAGS}"
                                                      fi
                                                      '''
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }
        archiveArtifacts allowEmptyArchive: true, artifacts: "${checkout_dir}/artifacts/*,${checkout_dir}/artifacts/**/*,${checkout_dir}/.kitchen/logs/kitchen.log"
    }
}


def run_pipeline() {
    def chunks = [:]
    def nox_passthrough_opts = "--log-cli-level=warning --ignore=tests/utils ${nox_passthrough_opts}"

    // Integration Module Tests
    for (int i=1; i<(integration_modules_chunks+1); i++) {
        def chunk_no = i
        def stagename = "Integration Modules #${chunk_no}"
        def env_array = [
            "NOX_PASSTHROUGH_OPTS=${nox_passthrough_opts} --test-group-count=$integration_modules_chunks --test-group=$chunk_no tests/integration/modules"
        ]
        chunks[stagename] = run_tests(stagename, env_array, parallel_testrun_timeout)
    }

    // Integration State Tests
    for (int i=1; i<(integration_states_chunks+1); i++) {
        def chunk_no = i
        def stagename = "Integration States #${chunk_no}"
        def env_array = [
            "NOX_PASSTHROUGH_OPTS=${nox_passthrough_opts} --test-group-count=$integration_states_chunks --test-group=$chunk_no tests/integration/states"
        ]
        chunks[stagename] = run_tests(stagename, env_array, parallel_testrun_timeout)
    }

    // Unit Tests
    for (int i=1; i<(unit_chunks+1); i++) {
        def chunk_no = i
        def stagename = "Unit #${chunk_no}"
        def env_array = [
            "NOX_PASSTHROUGH_OPTS=${nox_passthrough_opts} --test-group-count=$unit_chunks --test-group=$chunk_no tests/unit"
        ]
        chunks[stagename] = run_tests(stagename, env_array, parallel_testrun_timeout)
    }

    // All Other
    for (int i=1; i<(other_chunks+1); i++) {
        def chunk_no = i
        def stagename = "All Other #${chunk_no}"
        def env_array = [
            "NOX_PASSTHROUGH_OPTS=${nox_passthrough_opts} --test-group-count=$other_chunks --test-group=$chunk_no --ignore=tests/integration/modules --ignore=tests/integration/states --ignore=tests/unit"
        ]
        chunks[stagename] = run_tests(stagename, env_array, parallel_testrun_timeout)
    }


    timeout(time: global_timeout, unit: 'HOURS') {
        timestamps {
            withEnv([
                'SALT_KITCHEN_PLATFORMS=/var/jenkins/workspace/nox-platforms.yml',
                'SALT_KITCHEN_VERIFIER=/var/jenkins/workspace/nox-verifier.yml',
                'SALT_KITCHEN_DRIVER=/var/jenkins/workspace/driver.yml',
                "NOX_ENV_NAME=pytest-${test_transport.toLowerCase()}",
                'NOX_ENABLE_FROM_FILENAMES=true',
                "SALT_TARGET_BRANCH=${salt_target_branch}",
                "GOLDEN_IMAGES_CI_BRANCH=${golden_images_branch}",
                "CODECOV_FLAGS=${distro_name}${distro_version},${python_version},${test_transport.toLowerCase()}",
                'PATH=~/.rbenv/shims:/usr/local/rbenv/shims:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin:/root/bin',
                'RBENV_VERSION=2.4.2',
                "TEST_SUITE=${python_version}",
                "TEST_PLATFORM=${distro_name}-${distro_version}",
                "TEST_TRANSPORT=${test_transport}",
                "FORCE_FULL=${params.runFull}",
            ]) {

                githubNotify credentialsId: gh_commit_status_account,
                    description: "Testing ${distro_display_name} starts...",
                    status: 'PENDING',
                    context: gh_commit_status_context

                dir(checkout_directory) {
                    // Checkout the repo
                    stage('checkout-scm') {
                        cleanWs notFailBuild: true
                        checkout scm
                        sh 'git fetch --no-tags https://github.com/saltstack/salt.git +refs/heads/${SALT_TARGET_BRANCH}:refs/remotes/origin/${SALT_TARGET_BRANCH}'
                    }

                    // Setup the kitchen required bundle
                    stage('setup-bundle') {
                        sh 'bundle install --with ec2 windows --without docker macos opennebula vagrant'
                    }
                }

                try {
                    stage('Parallel Test Run') {
                        parallel chunks
                    }
                    stage('Serial Test Run') {
                        run_tests(
                            'Full Test Suite',
                            ["NOX_PASSTHROUGH_OPTS=${nox_passthrough_opts} tests/"],
                            serial_testrun_timeout
                        )
                    }
                } catch (Exception e) {
                    currentBuild.result = 'FAILURE'
                } finally {
                    cleanWs notFailBuild: true
                    if (currentBuild.resultIsBetterOrEqualTo('SUCCESS')) {
                        githubNotify credentialsId: gh_commit_status_account,
                            description: "Testing ${distro_display_name} succeeded",
                            status: 'SUCCESS',
                            context: gh_commit_status_context
                    } else {
                        githubNotify credentialsId: gh_commit_status_account,
                            description: "Testing ${distro_display_name} failed",
                            status: 'FAILURE',
                            context: gh_commit_status_context
                        try {
                          slackSend channel: "#jenkins-prod-pr",
                              color: '#FF0000',
                              message: "*${currentBuild.currentResult}*: ${currentBuild.getFullDisplayName()} (<${env.BUILD_URL}|open>)"
                        } catch (Exception e) {
                          sh 'echo Failed to send the Slack notification'
                        }
                    }
                }
            }
        }
    }
}

return this
// vim: ft=groovy
