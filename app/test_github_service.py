from app.services.github_service import GitHubService


service = GitHubService(".")


print("=" * 60)
print("CURRENT BRANCH")
print("=" * 60)

print(
    service.get_current_branch()
)


print("\n")
print("=" * 60)
print("BRANCHES")
print("=" * 60)

print(
    service.get_branches()
)


print("\n")
print("=" * 60)
print("STATUS")
print("=" * 60)

print(
    service.get_status()
)


print("\n")
print("=" * 60)
print("RECENT COMMITS")
print("=" * 60)

print(
    service.get_recent_commits()
)


print("\n")
print("=" * 60)
print("CHANGED FILES")
print("=" * 60)

print(
    service.get_changed_files()
)


print("\n")
print("=" * 60)
print("CONTRIBUTORS")
print("=" * 60)

print(
    service.get_commit_statistics()
)