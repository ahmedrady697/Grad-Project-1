# Contributing

Team of 6, four modules. These rules keep us from stepping on each other.

## Branches

- `main`: always working. Nobody pushes directly; everything goes through a Pull Request.
- `dev`: integration branch. Feature branches merge here first; `dev` is merged to `main` before each demo/milestone.
- Feature branches: `<module>/<short-description>`, for example:
  - `behavior/yolo-training`
  - `exam/gaze-estimation`
  - `attendance/face-enrollment`
  - `dashboard/live-feed-page`

## Workflow

```bash
git checkout dev
git pull
git checkout -b behavior/yolo-training
# ... work ...
git add .
git commit -m "behavior: add training script for YOLO"
git push -u origin behavior/yolo-training
```

Then open a Pull Request into `dev` and ask one teammate to review.

## Commit messages

Start with the module: `behavior:`, `exam:`, `attendance:`, `dashboard:`, `shared:`, `docs:`, `ci:`.

## Rules

1. **Never commit datasets, videos, or model weights.** Put them on Google Drive / Kaggle and document the link in `data/README.md`.
2. **Never commit secrets** (`.env`, API keys, passwords).
3. Only edit another module's folder after talking to its owner. Changes to `ai/shared/` need a review from everyone affected.
4. Every module outputs events using `ai/shared/schemas/event.py`. This is the contract with the dashboard. If you need a new field, change the schema in a separate PR first.
5. Keep notebooks in `notebooks/` inside your module and clear outputs before committing.
6. Run `ruff check .` and `pytest` before opening a PR (CI runs them too).

## Code style

- Python 3.10+, type hints where reasonable.
- Format and lint with `ruff`.
