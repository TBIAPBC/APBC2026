# A1 lecture prep

> Assumption used for this prep: A1 is the first assignment-oriented class after the introductory A0 session, so this note focuses on how to frame the course workflow, problem-solving expectations, Git/GitHub usage, testing, documentation, and peer review.  
> If A1 is actually tied to a different technical topic, this can be adapted quickly.

## Main goal of this lecture

Move students from "listening about the course" to "working in the course."

By the end of the lecture, students should understand that this subject is not mainly about learning syntax from scratch, but about using programming to solve biological/chemical problems in a structured, reproducible, collaborative way.

## What students should leave with

- They understand the workflow of the course.
- They know what a good solution looks like in this subject.
- They know how assignments, GitHub, review, and collaboration will work.
- They understand that code quality, documentation, and reasoning matter, not only getting the final answer.
- They are prepared to start A1 without being surprised by expectations.

## Core message to repeat during the lecture

Programming here is a research tool.

The aim is not:
- memorizing language features
- producing the shortest possible script
- hacking together something that only works once on one machine

The aim is:
- translating a problem into an algorithm
- implementing it clearly
- testing whether it behaves correctly
- documenting decisions
- making the solution readable for others
- using version control and review as part of the work

## Suggested lecture structure

## 1. Opening framing

Start by positioning A1 as the first "real" step into the course workflow.

Possible framing:
- In this course, students will solve concrete problems rather than passively absorb theory.
- Strong prior programming comfort is assumed.
- The course will also train habits that matter in real computational work: version control, documentation, reproducibility, and code review.
- A working solution is only one part of a good submission.

Emphasize that students who only focus on "making it run" will miss a substantial part of what is being evaluated.

## 2. What makes a strong submission

Define explicitly what you consider a strong solution.

### A strong solution should be:

- correct
- understandable
- modular enough to inspect
- documented
- testable
- reproducible
- reviewable by someone else

### A weak solution often looks like:

- hard-coded assumptions
- unclear variable names
- no explanation of input/output
- no edge-case handling
- no tests or examples
- no commit history showing development
- impossible for another student to review efficiently

This is a good place to explain that scientific programming is rarely judged only by the final output.

## 3. How to approach a programming problem

This part is worth making very explicit, because many students jump straight into coding.

### Recommended sequence

1. Understand the problem statement precisely.
2. Identify inputs, outputs, and constraints.
3. Break the task into smaller subproblems.
4. Write or sketch the algorithm before coding.
5. Implement incrementally.
6. Test on simple examples.
7. Handle edge cases.
8. Clean up names, structure, and comments.
9. Document usage.
10. Submit through the expected Git/GitHub workflow.

### Talking point

Students often fail not because they cannot code, but because they start coding before they have a clean model of the task.

## 4. Algorithmic thinking before implementation

This is a key educational point for A1.

Tell students that before writing code, they should be able to answer:

- What is the exact problem?
- What are the data objects?
- What steps transform input into output?
- Which parts may fail?
- What is the simplest correct version?
- How will I verify correctness?

This is a good place to contrast:

### "Implementation-first" mindset
- starts coding immediately
- discovers logic while writing code
- often produces messy structure

### "Algorithm-first" mindset
- defines steps first
- anticipates tricky cases
- leads to clearer implementation

## 5. Reproducibility and clarity as course values

Students in computational fields often underestimate reproducibility until something breaks.

Explain that in this course, reproducibility means:
- another person can obtain the same result
- input/output behavior is explicit
- assumptions are written down
- instructions are sufficient to run the solution
- repository state reflects development history

You can connect this to real scientific and industrial practice:
- unreproducible code is not trustworthy
- undocumented code is expensive
- unclear logic blocks collaboration

## 6. Git and GitHub are part of the learning objective

This part should be very concrete.

Students should understand that GitHub is not only a place to upload files. It is part of the workflow.

### Concepts worth stressing

- repository structure matters
- commit history matters
- commit messages matter
- review comments matter
- reading others' code matters
- asking questions on GitHub is part of the work

### Practical message

They are not only submitting answers. They are learning to work the way computational projects are actually developed.

## 7. Peer review expectations

Since review is part of the course, explain what good review looks like.

### Good review is not:
- "looks fine"
- only checking whether code runs
- superficial approval

### Good review is:
- checking correctness
- checking readability
- checking whether assumptions are stated
- trying edge cases
- asking clarifying questions
- identifying fragile parts
- suggesting concrete improvements

It may help to tell students that reviewing other code is one of the fastest ways to improve their own code quality.

## 8. Typical beginner mistakes even among technically strong students

This section helps normalize problems before they happen.

### Common mistakes

- solving a slightly different problem than the one assigned
- ignoring edge cases
- using unclear naming
- writing monolithic code with no structure
- skipping test examples
- documenting too little
- pushing disorganized repositories
- making last-minute commits with no meaningful history
- treating code review as bureaucracy instead of part of problem solving

You can say explicitly that a technically clever solution can still be weak if it is not communicable.

## 9. What to demonstrate live

A short live demonstration would help a lot here even if the lecture is mostly conceptual.

### Good demo options

#### Option A: from problem statement to algorithm sketch
Take a simple toy problem and show:
- how to extract the exact task
- how to define inputs/outputs
- how to write stepwise logic before code

#### Option B: bad vs good repository organization
Show two mini examples:
- one messy submission
- one clean submission

Compare:
- file names
- README quality
- code structure
- commit history
- ease of review

#### Option C: testing mindset
Take a tiny function and ask:
- what is the normal case?
- what are edge cases?
- what inputs might break it?

This is very effective because it trains them to think beyond the happy path.

## 10. Questions to ask students during class

Use these to make the lecture interactive.

- What makes code "good" beyond giving the correct output?
- How do you know your program is correct?
- What would another student need in order to review your work efficiently?
- What is an edge case in a task like this?
- Why is commit history useful?
- What makes documentation actually helpful rather than decorative?

These questions can reveal whether students are still thinking only in terms of final output.

## 11. Lecturer emphasis points

These are the points most worth repeating.

### Repeat clearly

- The course assumes prior coding comfort.
- The course is about applying programming, not learning basic programming from zero.
- Algorithm design matters before implementation.
- Reproducibility and documentation are evaluated values, not optional extras.
- GitHub workflow and peer review are part of the course content.
- Students should expect to read, test, and discuss other solutions.

## 12. Tone to set in the room

The best tone for A1 is:

- demanding but not hostile
- practical
- explicit about expectations
- supportive toward good-faith effort
- clear that professionalism matters

Students should feel:
- the course is serious
- expectations are high
- the rules are understandable
- success comes from disciplined work, not guessing what the instructor wants

## 13. Suggested closing

End with a short summary such as:

- Start from the problem, not from random code.
- Make your reasoning visible.
- Write code another person can inspect.
- Test it.
- Document it.
- Use Git/GitHub properly.
- Treat review as part of solving the task.

Then point students toward the assignment repository/workflow and remind them that the earlier they start, the easier it is to ask useful questions and improve through iteration.

## 14. Optional board / slide summary

### One-slide summary

#### In this course, a good solution is:
- correct
- algorithmically justified
- readable
- testable
- documented
- reproducible
- reviewable

#### Workflow
Problem -> algorithm -> implementation -> test -> document -> commit -> review

## 15. What to watch for while teaching

During the lecture, monitor whether students seem confused about:

- whether programming background is assumed
- whether GitHub is mandatory or only submission storage
- whether documentation affects evaluation
- whether peer review is serious
- whether they are expected to write tests
- whether code style matters

If any of these look unclear, state them again explicitly.

## 16. Compact speaker notes

### Key idea
This course teaches computational problem solving in practice.

### What students must understand
- not just code that runs
- code that others can inspect and reuse
- algorithmic reasoning first
- clear Git/GitHub workflow
- review is part of the method

### Key warning
Do not start by typing code before understanding the task.

### Key habit
Build the simplest correct version first, then improve it.

## 17. Very short version for yourself before class

If you need an ultra-short reminder right before teaching:

- Frame the course as applied computational problem solving.
- Emphasize strong prior coding expectation.
- Define what counts as a good submission.
- Stress algorithm before implementation.
- Explain reproducibility, documentation, and testing.
- Explain GitHub and peer review as real learning goals.
- End with clear expectations for starting A1.

## 18. Optional sentence bank for the lecture

You can reuse lines like these:

- "In this course, correctness is necessary, but it is not sufficient."
- "A solution that only works on your machine is not a strong computational solution."
- "If another student cannot understand or test your code, the job is not finished."
- "GitHub here is not only a delivery box; it is part of the working method."
- "Reviewing code is not separate from learning to code well."

## 19. If you want to connect A1 back to A0

A neat transition is:

A0 introduced the course mindset and showed that computational ideas can generate interesting behavior even with relatively simple models.  
A1 now shifts from inspiration to disciplined practice: how to actually solve problems, structure code, and collaborate professionally.

---
# Minimal checklist before lecture

- Confirm how A1 assignment/repository access will be communicated.
- Decide whether to show one live demo.
- Decide whether to show one bad-vs-good submission example.
- Prepare one slide or board sketch for the workflow:
  problem -> algorithm -> implementation -> test -> document -> review
- Be explicit about what is assumed and what is evaluated.