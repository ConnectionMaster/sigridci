Publishing your dependencies to Sigrid's Open Source Health
===========================================================

The [Sigrid CI documentation](../sigridci-integration/development-workflows.md) contains instructions on how you can integrate Sigrid into your development platform, which allows you to publish your code to Sigrid after every change. That section of the documentation contains instructions for common development platforms, for example GitHub or Azure DevOps.

This page contains some additional instructions on how you can best publish your system's open source libraries to Sigrid, so that they can be analyzed by Sigrid and shown in the [Open Source Health](system-open-source-health) page. The official, though somewhat obscure, term for this information is a [SBOM (Software Bill of Materials)](https://www.cisa.gov/sbom).

First of all, it is not necessary to submit the *binaries* for every library. If your system uses a dependency management tool, it is usually sufficient to send the corresponding configuration files. For example, Maven uses `pom.xml` to list dependencies, Gradle uses `build.gradle`, and NPM uses `package.json`. If any of those files are included in your repository, they will be picked up automatically. 

However, in some cases there might be extra options or caveats when using certain dependency management tools. The sections below contain some more specific instructions to take into consideration when using one of those dependency management tools. Also refer to [supported dependency management tools and open source ecosystems](../reference/supported-technologies.md) for a complete list of all supported technologies.

## Maven

### Maven properties

Maven properties are supported. It is quite common to define library versions as Maven properties:

    <properties>
        <guava.version>32.0.1-jre</guava.version>
    </properties>
    
And then refer to those properties when the dependency is defined.

    <dependency>
        <groupId>com.google.guava</groupId>
        <artifactId>guava</artifactId>
        <version>${guava.version}</version>
    </dependency>
    
Sigrid understands these properties, and will resolve dependencies to the correct version. This also works if the property is defined in the top-level POM, and then used in the module POMs.

### External parent POMs

Most Maven projects consist of multiple modules, which are then tied together by a "parent POM", which is basically just a top-level `pom.xml` that contains shared configuration across the entire project. 

In some cases, the parent POM itself *also* has a parent POM. This usually refers to a POM file which is shared across the entire organization, and tends to contain shared configuration across all projects in the organization. Having such an organization-wide used to be reasonably wide-spread, but is becoming increasingly rare as people move towards more independent repositories that do not have code dependencies on other repositories. 

Sigrid is able to scan the parent POM, but only if the parent POM is included in the source code that was published. And that's a problem, because as we just established these parent POMs are usually *not* part of the repository (by definition, as they contain all shared configuration across repositories). And if the parent POM is not published to Sigrid, then Sigrid is not able to read the file.

If you really want Sigrid to analyze your parent POM, you can include the [effective POM](help:effective-pom) in your upload. The effective POM is basically a standalone version of your project, without references to external files. You can generate the effective POM from the command line, as part of your build pipeline:

    mvn help:effective-pom 
    
Note that you need to run this command *before* you publish your code to Sigrid, otherwise the effective POM will not end up in the upload. Also note that it is sufficient to run this on-the-fly during your pipeline, it is not necessary to commit the effective POM to your repository.

## Gradle

Unlike most other dependency management tools, Gradle does not use a configuration file format like XML or JSON or YAML. Instead, it uses a full-blown programming language (originally Groovy, but Kotlin build scripts are also supported in newer versions). Gradle build scripts are therefore incredibly flexible, but they are also much harder to analyze for tools like Sigrid. 

If you use the configuration DSL to define your dependencies, Sigrid will automatically pick them up. 

    dependencies {
        api "com.google.code.gson:gson:2.8.8"
        testImplementation "org.junit.jupiter:junit-jupiter:5.7.2"
    }
    
Defining dependencies in this way will work just fine. However, there are much more flexible ways. You can define `ext` properties. You can define properties in `gradle.properties`. You can have full-blown Groovy/Kotlin logic. If you project uses these dynamic features, Sigrid might not be able to pick up all dependencies (again, it's hard to say where the line is exactly, since Gradle is so flexible).

However, Gradle also supports [lockfiles](https://docs.gradle.org/current/userguide/dependency_locking.html). These lockfiles define exactly which libraries and version are used by your projects, and are committed to your repository. If your codebase contains a Gradle lockfile, Sigrid will use this lockfile instead of `build.gradle`. This ensures Sigrid is able to extract all of your project's dependencies. Note that using a lockfile is a best practice even without considering Sigrid, as this allows for fully reproducible builds.

### NPM

NPM dependencies are defined in `package.json`, but NPM also generates a [lockfile](https://docs.npmjs.com/cli/v9/configuring-npm/package-lock-json) called `package-lock.json`. Since the lockfile defines the exact versions, Sigrid will prioritize the lockfile over the regular `package.json`.

### Yarn

Yarn is very similar to NPM, but its lockfile is called `yarn.lock` instead of NPM's `package-lock.json`. Like for NPM, Sigrid will prioritize the lockfile over `package.json` during its analysis.

### Other dependency management tools

This page provides some additional instructions and explanation for commonly used dependency management tools. For the complete list of all supportec technologies, refer to the [supported dependency management tools and open source ecosystems](../reference/supported-technologies.md).

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.
