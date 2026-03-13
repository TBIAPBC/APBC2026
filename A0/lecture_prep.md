# A0 lecturer notes — APBC first class

## Core teaching objective

A0 is not really about `Hello World` as a programming challenge.  
It is a controlled first contact with the full workflow the course will rely on:

- using the terminal
- reading an assignment carefully
- working in a Git repository
- creating a personal branch
- committing and pushing code
- opening a pull request
- using GitHub comments for help and review

That interpretation is strongly supported by the A0 README itself: the programming task is intentionally tiny, while most of the text is about GitHub registration, cloning, branching, committing, pushing, pull requests, and asking for help in PR comments.

A1 is the natural bridge from “can you submit code correctly?” to “can you read input, parse options, count, sort, and match exact output format?” with `-I` and `-l` as the first small examples of interface design. 

## What I would emphasize verbally

### 1. This course is about practical programming, not only syntax

Students may come in expecting a classic “learn Python/C++” course.  
You should state early that APBC is about solving problems with code and learning the working habits around code: command line usage, file handling, reproducibility, version control, review, and communication.

### 2. A0 is a workflow test, not an intelligence test

Say this explicitly. The task is supposed to be easy enough that cognitive load is spent on the environment and submission mechanics, not on algorithm design. That helps weaker students relax and stronger students understand why the task is intentionally simple.

### 3. Git branching is a safety mechanism

Students often experience branches as bureaucracy. Frame them as protection:

- your branch is your sandbox
- the base branch stays clean
- pull requests are the place for discussion
- review is part of development, not punishment

The Pro Git book remains a good conceptual source for explaining the working tree, staging area, repository, and the logic of branches. ([git-scm.com](https://git-scm.com/book/en/v2?utm_source=chatgpt.com))

### 4. Pull requests are the classroom interface

GitHub’s own docs define pull requests as the mechanism for proposing, reviewing, and merging changes, and PR reviews as the place where collaborators comment, approve, or request changes. That maps almost perfectly onto your course design. ([docs.github.com](https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests?utm_source=chatgpt.com))

## Suggested structure for the class

## Part 1 — Frame the course in 5–10 minutes

State:

- this is an assignment-driven course
- students are expected to work with Git/GitHub throughout
- discussion and review are part of the learning model
- the first class is about getting everyone operational

A useful message is:

> Today’s success criterion is not “write sophisticated code.”  
> Today’s success criterion is “get into the workflow and complete one clean submission.”

## Part 2 — Show the A0 task exactly in 5 minutes

Read the specification line by line:

- accept one file name on the command line
- print `Hello World!`
- add a line break after that line
- then print the file content
- do **not** add an extra line break at the end

That exactness matters because A0 quietly introduces an important habit: matching specification precisely, including output formatting. The sample input file is just `That's all folks!`, which makes it ideal for a quick live demo.

I would explicitly warn students that “almost correct output” is still wrong in automated checking.

## Part 3 — Live terminal demo in 15–20 minutes

Do one clean end-to-end demo yourself.

Suggested sequence:

````bash
git clone git@github.com:TBIAPBC/APBC2026.git
cd APBC2026
git config user.name "Your Name"
git config user.email "your@email"
git checkout -b yourgithubname-A0
````

Then create a tiny solution file, add it, commit it, and push it.

````bash
git add A0/yourgithubname-HelloWorld.py
git commit -m "Add A0 Hello World solution"
git push --set-upstream origin yourgithubname-A0
````

Then show the GitHub web UI and open a pull request.

This mirrors the A0 README workflow closely.

Two important lecturer notes here:

- check the actual default/base branch in the live repo before class; your inherited materials mention `master`, but many repositories now use `main`, so teach “the repository’s protected base branch” rather than hard-coding vocabulary unless you verify it live
- if the repo uses SSH, be prepared for authentication issues on student machines

GitHub’s official SSH docs are the right backup references for adding and testing SSH keys. ([docs.github.com](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?utm_source=chatgpt.com))

## Part 4 — Give students a minimal shell survival kit in 5–10 minutes

Do not turn this into a shell lecture.  
Only teach the commands they need today:

- `pwd`
- `ls`
- `cd`
- opening/editing a file
- maybe `cat`

Software Carpentry’s shell lessons are a good background reference for this level: shell intro, navigating files/directories, creating/moving files, and a compact command summary. ([swcarpentry.github.io](https://swcarpentry.github.io/shell-novice/01-intro.html?utm_source=chatgpt.com))

The teaching principle here is to reduce environmental panic. Students do not need shell mastery on day 1; they need enough shell to complete A0.

## Part 5 — Make the social contract explicit

Tell students where to ask what:

- general course questions → issues or general repo discussion space
- submission-specific help → comments in their PR
- review requests → PR reviewers / PR comments
- mention people with `@username` when needed

This is already built into the A0 materials, which explicitly instruct students to use PR comments for help and to request review once ready. :contentReference[oaicite:6]{index=6}

I would say this explicitly:

> In this course, asking a good technical question in GitHub is itself part of the skill we are practicing.

## Common failure points to anticipate

### GitHub access / permissions

Some students will not yet have organization access or will not know their GitHub username.

### SSH setup

Expect this to be the biggest time sink if students work on their own laptops.  
Have one fallback ready:

- either an HTTPS cloning path
- or a prewritten SSH troubleshooting handout

### Wrong branch

Some students will accidentally commit on the base branch or forget to switch.

### Wrong filename / wrong directory

A0 already fixes naming conventions, so expect mistakes like:

- wrong suffix
- wrong directory
- wrong GitHub handle in filename

### Output formatting

The most subtle bug in A0 is the “no extra newline” requirement.

### Confusion between “commit” and “push”

Students often think commit automatically uploads to GitHub.  
Make the distinction explicit:

- `commit` = saved in local Git history
- `push` = sent to remote repository

That distinction is part of the standard Git mental model described in Pro Git. ([git-scm.com](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F?utm_source=chatgpt.com))

## Best way to position review culture

GitHub’s docs treat PR review as a normal collaboration mechanism for commenting, suggesting changes, approving, and requesting changes. ([docs.github.com](https://docs.github.com/articles/about-pull-request-reviews?utm_source=chatgpt.com))

For APBC, I would frame review in three layers:

1. **correctness** — does it work?
2. **specification compliance** — does it match the exact assignment?
3. **readability** — could another student understand and test it?

That framing is helpful because beginners otherwise think review only means “find bugs.”

## External materials worth using for your prep

These are the ones I would actually rely on:

### Git concepts

- **Pro Git book** for the cleanest explanation of Git basics, first-time setup, remotes, and branching. ([git-scm.com](https://git-scm.com/book/en/v2?utm_source=chatgpt.com))

### GitHub workflow

- **About pull requests**
- **About pull request reviews**
- **Creating a pull request**
- **Requesting a pull request review**  
  These align directly with the A0 submission model. ([docs.github.com](https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests?utm_source=chatgpt.com))

### Authentication

- **Adding a new SSH key to GitHub**
- **Testing your SSH connection** ([docs.github.com](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account?utm_source=chatgpt.com))

### Shell refresher

- **Software Carpentry: Shell Novice** for exactly the subset of shell knowledge students need on day 1. ([swcarpentry.github.io](https://swcarpentry.github.io/shell-novice/?utm_source=chatgpt.com))

### One-page handout

- **GitHub Education Git cheat sheet** as a compact reference for students during the first two assignments. ([education.github.com](https://education.github.com/git-cheat-sheet-education.pdf?utm_source=chatgpt.com))

### Pedagogical design hint

GitHub Skills’ instructor guidance is useful mainly for one idea: keep early learning tasks focused, concrete, and broken into small steps, and link out to documentation instead of overloading the session. That matches A0 very well. ([skills.github.com](https://skills.github.com/quickstart?utm_source=chatgpt.com))

## Recommended lecturer script for the end of class

You want students to leave knowing exactly what “done” means.

A good closing message is:

> Before next class, your goal is:
> 1. complete A0,
> 2. push it to your own branch,
> 3. open a pull request,
> 4. and use GitHub comments if anything blocks you.

Then briefly preview A1 as the next step:

- reading files
- command-line options
- counting
- sorting
- exact output matching :contentReference[oaicite:7]{index=7}

That makes the transition feel intentional rather than abrupt.

## One-sentence summary for you

Teach A0 as **workflow onboarding with a tiny coding task attached**, not as a programming exercise with some Git on the side.