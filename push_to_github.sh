#!/bin/bash

# Script to push the Movie Database Application to GitHub
# with local changes as priority

echo "Pushing Movie Database Application to GitHub..."

# Check if the remote already exists and remove it if it does
if git remote | grep -q "origin"; then
  echo "Remote 'origin' already exists. Removing it..."
  git remote remove origin
fi

# Add the GitHub repository as a remote named "origin"
echo "Adding GitHub repository as remote 'origin'..."
git remote add origin git@github.com:rtaran/movie-project-phase-2.git

# Verify that the remote was added correctly
echo "Verifying remote..."
git remote -v

# Configure Git to use merge strategy for pulls
echo "Configuring Git to use merge strategy for pulls..."
git config pull.rebase false

# Pull from the remote repository first to integrate any existing changes
echo "Pulling from GitHub to integrate any existing changes..."
git pull --allow-unrelated-histories origin main || echo "No remote changes to pull or pull failed. Continuing..."

# Push your local repository to GitHub, setting the local main branch to track the remote main branch
echo "Pushing to GitHub..."
git push -f -u origin main

echo "Done! Your Movie Database Application is now on GitHub."
echo "Repository URL: https://github.com/rtaran/movie-project-phase-2"
