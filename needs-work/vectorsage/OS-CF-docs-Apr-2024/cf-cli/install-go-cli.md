# Installing the cf CLI
The cf CLI is the official command line client for Cloud Foundry.
The following procedures describe how to install the cf CLI on your operating system. You can install the cf CLI with a package manager, an installer, or a compressed binary.
For more information about how to use the cf CLI, see [Getting Started with cf CLI](https://docs.cloudfoundry.org/cf-cli/getting-started.html).
To learn when cf CLI updates are released and to download a new binary or installer, see [Releases](https://github.com/cloudfoundry/cli/releases) in the Cloud Foundry CLI repository on GitHub.
There are currently two major versions of the cf CLI: v7 and v8. See [the README](https://github.com/cloudfoundry/cli/blob/master/README.md) to decide which version to use.

## Prerequisites
If you previously used the cf CLI Ruby gem, you must uninstall the gem before installing the cf CLI.
To uninstall the gem:

1. Run:
```
gem uninstall cf
```

2. Verify that your Ruby environment manager uninstalled the gem by closing and reopening your terminal.

## Install the cf CLI using a package manager
These sections describe how to install the cf CLI using a package manager. You can install the cf CLI using a package manager on Mac OS X and Linux operating systems.

### Linux installation
There are two ways to install the cf CLI using a package manager, depending on your Linux distribution.
To install the cf CLI on Debian and Ubuntu-based Linux distributions:

1. Add the Cloud Foundry Foundation public key and package repository to your system by running:
```
wget -q -O - https://packages.cloudfoundry.org/debian/cli.cloudfoundry.org.key | sudo apt-key add -
echo "deb https://packages.cloudfoundry.org/debian stable main" | sudo tee /etc/apt/sources.list.d/cloudfoundry-cli.list
```

2. Update your local package index by running:
```
sudo apt-get update
```

3. To install **cf CLI v7**, run:
```
sudo apt-get install cf7-cli
```

4. To install **cf CLI v8**, run:
```
sudo apt-get install cf8-cli
```
To install the cf CLI on Enterprise Linux and Fedora RHEL6/CentOS6 and later distributions:

1. Configure the Cloud Foundry Foundation package repository by running:
```
sudo wget -O /etc/yum.repos.d/cloudfoundry-cli.repo https://packages.cloudfoundry.org/fedora/cloudfoundry-cli.repo
```

2. To install **cf CLI v7**, run:
```
sudo yum install cf7-cli
```

3. To install **cf CLI v8**, run:
```
sudo yum install cf8-cli
```
This also downloads and adds the public key to your system.

### Mac OS X installation
You can install the cf CLI on Mac OS X operating systems using the Homebrew package manager.
To install the cf CLI for Mac OS X using Homebrew:

1. Install Homebrew. For instructions, see [Install Homebrew](http://brew.sh/) on the Homebrew website.

2. To install **cf CLI v7**, run:
```
brew install cloudfoundry/tap/cf-cli@7
```

3. To install **cf CLI v8**, run:
```
brew install cloudfoundry/tap/cf-cli@8
```

## Install the cf CLI using a compressed binary
You can install the cf CLI using a compressed binary on Windows, Mac OS X, and Linux operating systems.
In cases where security concerns are paramount, using this method can be a better option than installing from a repository.

**Note**
As of CF CLI 8.4.0 and CF CLI 7.5.0, the Apple ARM architecture is now supported for installation of CF CLI. This is possible on newer MACs that use M1 and M2 processors. For systems running the M1 processor, CF CLI can now be installed without use of an emulator.
For more information about downloading and installing a compressed binary for cf CLI v7 or cf CLI v8, see [Installers and compressed binaries](https://github.com/cloudfoundry/cli/wiki/V8-CLI-Installation-Guide#installers-and-compressed-binaries).

## Verify installation
To verify the installation of the cf CLI:

1. Close and reopen the command prompt. Or, open a new tab in the command prompt.

2. Run:
```
cf --help
```
If your installation was successful, the cf CLI help listing appears.

## Uninstall the cf CLI
These sections describe how to uninstall the cf CLI. The method for uninstalling the cf CLI differs depending on the installation method.

### Package manager
If you installed the cf CLI with a package manager, follow the instructions specific to your package manager.

### Installer
If you installed the cf CLI with an installer, follow the procedure in this section that is specific to your operating system.
To uninstall the cf CLI on Mac OS X:

1. Delete the binary `/usr/local/bin/cf`.

2. Delete the directory `/usr/local/share/doc/cf-cli`.
To uninstall the cf CLI on Windows:

1. Go to the **Control Panel** and click **Programs and Features**.

2. Select **Cloud Foundry CLI VERSION**.

3. Click **Uninstall**.

### Binary
To uninstall the cf CLI after installing it with a binary:

1. Go to the location where you copied the binary.

2. Delete the binary.