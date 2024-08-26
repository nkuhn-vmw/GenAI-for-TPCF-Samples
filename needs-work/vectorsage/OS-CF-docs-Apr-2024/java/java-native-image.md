# Using Java Native Image in Cloud Foundry
You can build your Java apps with native image support and deploy those apps to Cloud Foundry.
A growing number of Java users are building Java apps using support for native images.
For more information, see [Native Image](https://www.graalvm.org/reference-manual/native-image/) in the GraalVM documentation.
Java users deploying to Cloud Foundry can deploy apps compiled using native image support.
However, the Cloud Foundry Java buildpack does not provide support to build, compile, and turn apps into a native image.
You must perform those steps before deploying to Cloud Foundry.
To build your app that is suitable for running on Cloud Foundry you can do one of the following:

* [Build using Cloud Native Buildpacks](https://docs.cloudfoundry.org/buildpacks/java/java-native-image.html#cloud-native-buildpacks)

* [Build using native build tools](https://docs.cloudfoundry.org/buildpacks/java/java-native-image.html#native-build-tools)

## Building using Cloud Native Buildpacks
Cloud Native Buildpacks include support for building native image apps.
You can pass in your source code or a compiled JAR and Cloud Native Buildpacks installs the required tools and builds a compatible image.

### Using Cloud Native Buildpacks example

1. Clone the example repository from GitHub:
```
git clone https://github.com/paketo-buildpacks/samples
cd samples/java/native-image/java-native-image-sample
```

2. Build the example image:
```
./mvnw package
pack build apps/native-image -p target/demo-0.0.1-SNAPSHOT.jar -e BP\_NATIVE\_IMAGE=true -B paketobuildpacks/builder:tiny
```
For more information about building with Cloud Native Buildpacks, see [Getting Started](https://docs.spring.io/spring-native/docs/current/reference/htmlsingle/#getting-started-buildpacks) in the Spring Native documentation.

### Deploying using Cloud Native Buildpacks
This section describes how to deploy a Java app with native image support using Cloud Native Buildpacks.
To deploy an app compiled using the steps from the previous section to Cloud Foundry, you can deploy the image directly using Cloud Foundry’s Docker support.
If Docker support is deactivated, you can extract the native image binary from the container image and deploy the app using the binary buildpack.

#### Deploying from an image
To deploy the app from an image:

1. Publish your image. You can do this in a number of ways. For example, you can use the `--publish` flag to `pack build` with `docker tag` and `docker push`, or through any other means of publishing a container image to a registry.

2. Validate that your foundation supports deploying Docker images by running the following command and confirming that `diego_docker` is set to `enabled`. If it is set to `disabled`, you cannot use this deployment option.
```
cf feature-flags
```
For example:
```
$ cf feature-flags
Retrieving status of all flagged features as [user@example.com](mailto:user@example.com)...
```
features state
user\_org\_creation disabled
private\_domain\_creation enabled
app\_bits\_upload enabled
app\_scaling enabled
route\_creation enabled
service\_instance\_creation enabled
diego\_docker enabled
set\_roles\_by\_username enabled
unset\_roles\_by\_username enabled
task\_creation enabled
env\_var\_visibility enabled
space\_scoped\_private\_broker\_creation enabled
space\_developer\_env\_var\_visibility enabled
service\_instance\_sharing enabled
hide\_marketplace\_from\_unauthenticated\_users disabled
resource\_matching enabled

3. Push your app by running:
```
cf push -o registry.example.com/apps/native-image native-image-app
```

#### Extracting the image and deploy the Binary buildpack
To extract and deploy your app using the binary buildpack:

1. Create a script to extract the files:
```

#!/bin/bash
if [ -z "$1" ] || [ -z "$2" ]; then
echo "USAGE: extract.sh image-name full-main-class"
echo
exit 1
fi
CONTAINER\_ID=$(docker create "$1")
mkdir -p ./out
docker cp "$CONTAINER\_ID:/workspace/$2" "./out/$2"
docker rm "$CONTAINER\_ID" > /dev/null
```
This script is optional, but illustrates the process of extracting the binary file.
It runs `docker create` and `docker cp` to extract the file from the image, followed by `docker rm` to remove the containerd.
You can do this manually, or you can use any other tools for interacting with a container image.

2. Run the extract script:
```
$ ./extract.sh apps/native-image io.paketo.demo.Demoapp
$ file ./out/io.paketo.demo.Demoapp
io.paketo.demo.Demoapp: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=05cb81992f3859c9653a9ef6a691e798a9c48b9b, with debug_info, not stripped
```
The extract script places the binary in a directory called `out` under the current working directory.
You can run `file` to examine it and confirm that it is a 64-bit Linux executable.

3. Push and run the compiled binary by running the following command. You can adjust other properties or use a `manifest.yml` file to deploy as well.
```
cf push -b binary_buildpack -m 256M -p ./out -c ./io.paketo.demo.Demoapp native-image
```

## Building using Native Build Tools
This section describes how to deploy a Java app with native image support using Native Build Tools.
If you do not want to build using Cloud Native Buildpacks, you can build and compile directly using the Native Build Tools.
To build a Java app using Native Build Tools:

1. Obtain an Ubuntu Bionic computer, VM, or container.
Ubuntu Bionic is recommended for best compatibility with the Cloud Foundry `cflinuxfs3` root filesystem.
Ubuntu 22.04 LTS (Jammy Jellyfish) is recommended for use with `cflinuxfs4`.

2. Install GraalVM. See [Get Started with GraalVM](https://www.graalvm.org/docs/getting-started/).

3. Install the Java Native Image tools. See [Install Native Image](https://www.graalvm.org/reference-manual/native-image/#install-native-image).

4. To add the Native Build Tools to your Maven or Gradle project, follow the instructions in [Add the native build tools plugin](https://docs.spring.io/spring-native/docs/current/reference/htmlsingle/#_add_the_native_build_tools_plugin) in the Spring documentation. This only needs to be done once.

5. Clone the example repository from GitHub:
```
git clone https://github.com/paketo-buildpacks/samples
cd samples/java/native-image/java-native-image-sample
```

6. Build the example image:
```
mvn -Pnative -DskipTests package
```
For more information about building with Native Build Tools, see [Getting started with native build tools](https://docs.spring.io/spring-native/docs/current/reference/htmlsingle/#getting-started-native-build-tools) in the Spring documentation.

### Deploying with direct build
This section describes how to deploy a Java app with native image support using a direct build.
To deploy a Java app with native image support using the binary buildpack:

1. Zip the executable created by your build tool, either Maven or Gradle.
For example, with Maven, `zip demo.zip target/demo`.
Alternatively, you can copy the executable into a directory by itself.
For example, with Maven, `mkdir -p ./out && cp target/demo ./out/`.
This is the root for `cf push`.

2. Push the root ZIP file or directory you created in the previous step.
If you use a directory instead of a ZIP archive, adjust the `-p` argument.
This is important so that it only uploads the compiled binary, not your entire project.
You can adjust other properties or use a `manifest.yml` file to deploy as well.
```
cf push -b binary_buildpack -p demo.zip -c ./target/demo native-image
```

## Spring Boot and Spring Native
Regardless of how you build your app, with Spring Boot v2.5 and Spring Native v0.10.1, there is a bug that causes `cf push` to fail.
The problem is caused by conditional behavior in Spring Boot Actuator when run on Cloud Foundry. It is fixed in Spring Native v0.10.2.
For more information, see the [spring-projects-experimental](https://github.com/spring-projects-experimental/spring-native/issues/870) repository on GitHub.
You can also work around this issue by adding the following hints above your `@SpringBootapp` annotation:
For example:
```
@NativeHint(trigger = ReactiveCloud FoundryActuatorAutoConfiguration.class, types = {
@TypeHint(types = EndpointCloud FoundryExtension.class, access = AccessBits.ANNOTATION),
@TypeHint(typeNames = "org.springframework.boot.actuate.autoconfigure.Cloud Foundry.Cloud FoundryEndpointFilter"),
@TypeHint(typeNames = "org.springframework.boot.actuate.autoconfigure.Cloud Foundry.reactive.Cloud FoundryWebFluxEndpointHandlerMapping$Cloud FoundryLinksHandler", access = AccessBits.LOAD\_AND\_CONSTRUCT
| AccessBits.DECLARED\_METHODS) })
@NativeHint(trigger = Cloud FoundryActuatorAutoConfiguration.class, types = {
@TypeHint(types = EndpointCloud FoundryExtension.class, access = AccessBits.ANNOTATION),
@TypeHint(typeNames = "org.springframework.boot.actuate.autoconfigure.Cloud Foundry.Cloud FoundryEndpointFilter"),
@TypeHint(typeNames = "org.springframework.boot.actuate.autoconfigure.Cloud Foundry.servlet.Cloud FoundryWebEndpointServletHandlerMapping$Cloud FoundryLinksHandler", access = AccessBits.LOAD\_AND\_CONSTRUCT
| AccessBits.DECLARED\_METHODS) })
@SpringBootapp
public class Demoapp {
public static void main(String[] args) {
Springapp.run(Demoapp.class, args);
}
}
```