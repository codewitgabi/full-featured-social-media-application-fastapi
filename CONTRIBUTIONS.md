<!-- Guidelines to project contribution -->

#### First steps

- Create a fork of the project.
- Create a branch for the feature you're implementing.
- Every feature must have a separate branch.

#### Guidelines

- Every branch must do one thing and one thing only.
    - `FIXES AND UPDATES CANNOT NOT BE IN THE SAME BRANCH`
- Feature names should be descriptive and unique and so should your branch names e.g `feature/create-user-account`, `feature/update-user-account`, `bugfix/fix-model-migrations`.
- Pull requests should be made to the `dev` branch as any `PR `made to the `main` branch directly would be closed.
- Pull requests should follow standard conventions e.g `feat: added endpoint for user creation`, `fix: removed deprecated features`.
- **Every** feature must have tests for it and those tests must pass together with existing ones.
- Wait for your `PR` to be approved and merged by project maintainers.
