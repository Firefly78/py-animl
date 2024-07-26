
# Notes to self on how to publish

(will have to streamline this later).


1. Create new branch named: "release-0.x.x"
2. Run the following commands:
    - `git checkout release-0.x.x`
    - `bumpver update --major/minor/patch`
    - `git push origin release-0.x.x --tags`

3. Create a pull request from "release-0.x.x" to "main" branch.
4. Complete the merge request.

5. Got to [github](https://github.com/Firefly78/py-animl)
6. Click "Create new release"
7. Choose the tag you just created.
8. Click "Generate release notes"
9. Click "Publish release"
