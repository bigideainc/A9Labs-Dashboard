import json
from huggingface_hub import HfApi, Repository, hf_hub_download
from datetime import datetime
from typing import List, Dict, Optional
import os

def fetch_training_metrics_commits(repo_id: str, token: Optional[str] = None) -> List[Dict]:
    """
    Fetch training metrics from a Hugging Face repository.
    
    Args:
        repo_id (str): The repository ID
        token (Optional[str]): Hugging Face API token
    """
    try:
        api = HfApi(token=token)
        commits = api.list_repo_commits(repo_id=repo_id)

        training_metrics = []
        processed_commits = 0

        print(f"Found {len(commits)} total commits in repository")

        for commit in commits:
            try:
                files = api.list_repo_tree(
                    repo_id=repo_id, 
                    revision=commit.commit_id
                )
                json_files = [f for f in files if f.path.endswith('.json')]

                for json_file in json_files:
                    try:
                        local_path = hf_hub_download(
                            repo_id=repo_id,
                            filename=json_file.path,
                            revision=commit.commit_id,
                            token=token
                        )

                        with open(local_path, 'r') as f:
                            metrics_data = json.loads(f.read())

                        if isinstance(metrics_data, dict) and "metrics" in metrics_data:
                            miner_uid = metrics_data.get("miner_uid")
                            job_id = metrics_data["metrics"].get("job_id")

                            if miner_uid and job_id:
                                metrics_entry = {
                                    "model_repo": metrics_data.get("model_repo", "unknown"),
                                    "metrics": metrics_data["metrics"],
                                    "miner_uid": miner_uid,
                                    "job_id": job_id,
                                    "timestamp": metrics_data.get("timestamp", "unknown")
                                }
                                training_metrics.append(metrics_entry)
                                processed_commits += 1

                    except Exception as e:
                        print(f"Error processing file {json_file.path}: {str(e)}")
                        continue

            except Exception as e:
                print(f"Error processing commit {commit.commit_id}: {str(e)}")
                continue

        filtered_metrics = [
            entry for entry in training_metrics 
            if entry.get('miner_uid') and entry['metrics'].get('job_id')
        ]

        print(f"Successfully processed {processed_commits} commits with valid metrics")
        return filtered_metrics

    except Exception as e:
        print(f"Error fetching commits: {str(e)}")
        return []

