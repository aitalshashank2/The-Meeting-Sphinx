## Contributing guidelines

Thank you for your interest in contributing to The-Meeting-sphinx! Here are a few pointers about how you can help.

### Setting things up

To set up the development environment, follow the instructions in README.

### Finding something to work on

The issue tracker of The-Meeting-Sphinx is a good place to start. If you find something that interests you, comment on the thread and we'll help you get started.

Alternatively, if you came across a new bug or have thought of a new feature, please file an issue and comment if you would like to be assigned.

If neither of these seem appealing, please reach out to any of us on our emails.

### Instructions to submit code

1. Create a new branch off `master`. Select a descriptive branch name.
```bash
git remote add upstream git@github.com:aitalshashank2/The-Meeting-Sphinx.git
git fetch upstream
git checkout master
git merge upstream/master
git checkout -b your-branch-name
```

2. Commit and push code to your branch

- Commits should be self-contained and contain a descriptive commit message.

3. Once the code is pushed, create a pull request

- On your GitHub fork, select your branch and click `New Pull Request`. Select `master` as the base branch and add your branch in the `compare` dropdown. If the code is mergable, you get a message saying **Able to merge**. Go ahead and create a pull request.
- Once you have created a pull request, a reviewer will review your Pull Request and merge your Pull Request if he/she approves.

Congratulations! You have successfully contributed to Project `The-Meeting-Sphinx`!
