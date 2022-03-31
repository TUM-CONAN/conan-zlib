def artifactory_name = "conan.campar.in.tum.de"
def artifactory_repo = "conan-camposs"
def repo_url = 'https://github.com/TUM-CONAN/conan-zlib.git'
def repo_branch = "stable/1.2.12"
def recipe_folder = "."
def recipe_version = "1.2.12"

node {
    def server = Artifactory.server artifactory_name
    def client = Artifactory.newConanClient()
    def serverName = client.remote.add server: server, repo: artifactory_repo

    stage("Get recipe"){
        git branch: repo_branch, url: repo_url
    }

    stage("Test recipe"){
        dir (recipe_folder) {
          client.run(command: "create . ${recipe_version}@camposs/stable")
        }
    }

    stage("Upload packages"){
        String command = "upload \"*\" --all -r ${serverName} --confirm"
        def b = client.run(command: command)
        server.publishBuildInfo b
    }
}
