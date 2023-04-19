pipeline {
    environment {
        REGISTRY = 'ghcr.io'
        NAMESPACE = 'changhwi-hong'
        IMAGE_NAME = 'webapp'
    }
    agent any
    stages{
        stage("checkout") {
            steps {
                checkout scm
            }
        }
        
        stage("build and push image") {
            steps {
                withDockerRegistry(url: 'https://ghcr.io', credentialsId: 'github-creds') {
                    sh 'docker build . -t ${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${BUILD_NUMBER}'
                    sh 'docker push ${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${BUILD_NUMBER}'
                }
            }
        }
        
        stage("clean up image") {
            steps {
                sh 'docker rmi ${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${BUILD_NUMBER}'
            }
        }

        stage("update manifest") {
            agent {
                docker { image 'argoproj/argo-cd-ci-builder:latest' }
            }
            steps {
                checkout changelog: false, poll: false, scm: scmGit(
                    branches: [[name: '*/main']], 
                    extensions: [], 
                    userRemoteConfigs: [[credentialsId: 'github-creds', url: 'https://github.com/changhwi-hong/web-app-manifest.git']])
                
                withCredentials([gitUsernamePassword(credentialsId: 'github-creds', gitToolName: 'Default')]) {
                    sh """
                        git config user.email "changhwi.hong@bespinglobal.com"
                        git config user.name "changhwi-hong"
                        kustomize edit set image ${REGISTRY}/${NAMESPACE}/${IMAGE_NAME}:${BUILD_NUMBER}
                        cat kustomization.yaml
                        git commit -a -m "updated the image tag to ${BUILD_NUMBER}"
                        git push origin HEAD:main
                    """
                }
               
            }
        }
    }
}
