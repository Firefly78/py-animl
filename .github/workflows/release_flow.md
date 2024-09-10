
# Notes to self on how to publish


1. Create feature branches from "dev" branch, either from issues or stand-alone
2. Create pull requests from feature branches to "dev" branch, perform review
3. Locally, run the following commands:
    - `git checkout dev`
    - `bumpver update --major/minor/patch`
    - `git push`
    - `git push --tags`

4. Create a pull request from "dev" to "main" branch, with the title: `PR: release-x.x.x`
5. Complete the merge request.

6. Got to [github](https://github.com/Firefly78/py-animl)
7. Click "Create new release"
8. Choose the tag you just created.
9. Click "Generate release notes"
10. Click "Publish release"
