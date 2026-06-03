from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import engine
from database import get_db

import models
import schemas

from github_service import fetch_repo


# Create database tables automatically
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GitHub Repository Analyzer",
    description="Analyze GitHub repositories and store analytics",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "GitHub Repository Analyzer Running"
    }


@app.post("/analyze")
def analyze_repository(
    repo: schemas.RepoRequest,
    db: Session = Depends(get_db)
):

    data = fetch_repo(
        repo.owner,
        repo.repo_name
    )

    if not data:

        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    existing_repo = (
        db.query(models.Repository)
        .filter(
            models.Repository.owner == repo.owner,
            models.Repository.repo_name == repo.repo_name
        )
        .first()
    )

    if existing_repo:

        return {
            "message": "Repository already stored",
            "repository": existing_repo.repo_name,
            "stars": existing_repo.stars
        }

    new_repo = models.Repository(
        owner=data["owner"]["login"],
        repo_name=data["name"],
        stars=data["stargazers_count"],
        forks=data["forks_count"],
        open_issues=data["open_issues_count"],
        language=data["language"]
    )

    db.add(new_repo)

    db.commit()

    db.refresh(new_repo)

    return {
        "message": "Repository analyzed successfully",
        "owner": new_repo.owner,
        "repository": new_repo.repo_name,
        "stars": new_repo.stars,
        "forks": new_repo.forks,
        "open_issues": new_repo.open_issues,
        "language": new_repo.language
    }


@app.get("/repositories")
def get_all_repositories(
    db: Session = Depends(get_db)
):

    repos = db.query(
        models.Repository
    ).all()

    return repos


@app.get("/repository/{repo_id}")
def get_repository(
    repo_id: int,
    db: Session = Depends(get_db)
):

    repo = (
        db.query(models.Repository)
        .filter(
            models.Repository.id == repo_id
        )
        .first()
    )

    if not repo:

        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    return repo


@app.delete("/repository/{repo_id}")
def delete_repository(
    repo_id: int,
    db: Session = Depends(get_db)
):

    repo = (
        db.query(models.Repository)
        .filter(
            models.Repository.id == repo_id
        )
        .first()
    )

    if not repo:

        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    db.delete(repo)

    db.commit()

    return {
        "message": "Repository deleted successfully"
    }


@app.get("/top")
def get_top_repository(
    db: Session = Depends(get_db)
):

    repo = (
        db.query(models.Repository)
        .order_by(
            models.Repository.stars.desc()
        )
        .first()
    )

    if not repo:

        return {
            "message": "No repositories found"
        }

    return {
        "owner": repo.owner,
        "repository": repo.repo_name,
        "stars": repo.stars
    }


@app.get("/statistics")
def repository_statistics(
    db: Session = Depends(get_db)
):

    repos = db.query(
        models.Repository
    ).all()

    total_repositories = len(repos)

    if total_repositories == 0:

        return {
            "total_repositories": 0,
            "average_stars": 0
        }

    total_stars = sum(
        repo.stars for repo in repos
    )

    average_stars = (
        total_stars / total_repositories
    )

    return {
        "total_repositories": total_repositories,
        "total_stars": total_stars,
        "average_stars": round(
            average_stars,
            2
        )
    }