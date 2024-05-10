# Merging with upstream buildpacks
Learn how to maintain your forked buildpack by merging it with the upstream Cloud Foundry buildpack.
This process keeps your fork updated with changes from the original buildpack, providing patches, updates, and new features.
The following procedure assumes that you are maintaining a custom buildpack that was forked from
a Cloud Foundry system buildpack. However, you can use the same procedure to update a buildpack forked from any upstream buildpack.
To sync your forked buildpack with an upstream Cloud Foundry buildpack:

1. Go to your forked repository on GitHub and click **Compare**. The **Comparing changes** page shows the unmerged commits between your forked buildpack and the upstream buildpack. Inspect unmerged commits and confirm that you want to merge them all.

2. Go to the forked repository and set the upstream remote as the Cloud Foundry buildpack repository.
```
$ cd ~/workspace/ruby-buildpack
$ git remote add upstream git@github.com:cloudfoundry/ruby-buildpack.git
```

3. Pull down the remote upstream changes.
```
$ git fetch upstream
```

4. Merge the upstream changes into the intended branch. You might need to resolve merge conflicts.
This example shows the merging of the `main` branch of the upstream buildpack into the `main` branch of the forked buildpack.
```
$ git checkout main
$ git merge upstream/main
```

**Important**
When you merge upstream buildpacks, do not use `git rebase`.
This approach is not sustainable because you confront the same merge conflicts repeatedly.

5. Run the buildpack test suite to ensure that the upstream changes do not break anything.
```
$ BUNDLE_GEMFILE=cf.Gemfile buildpack-build
```

6. Push the updated branch.
```
$ git push
```
Your forked buildpack is now synced with the upstream Cloud Foundry buildpack.
For more information about syncing forks, see [Syncing a fork](https://help.github.com/articles/syncing-a-fork/).