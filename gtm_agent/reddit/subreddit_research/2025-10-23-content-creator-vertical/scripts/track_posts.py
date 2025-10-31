#!/usr/bin/env python3
"""
Post Tracking Script
Tracks Reddit post performance and generates reports
"""

import csv
import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path

class PostTracker:
    """Track Reddit post performance"""

    def __init__(self, output_dir: str = "."):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.tracking_file = self.output_dir / "post_tracking.json"
        self.csv_file = self.output_dir / "performance_tracking.csv"

        self.posts = self.load_posts()

    def load_posts(self) -> List[Dict]:
        """Load existing post data"""
        if self.tracking_file.exists():
            with open(self.tracking_file, "r") as f:
                return json.load(f)
        return []

    def save_posts(self):
        """Save post data to JSON"""
        with open(self.tracking_file, "w") as f:
            json.dump(self.posts, f, indent=2)

    def add_post(self, subreddit: str, title: str, url: str, post_type: str = "main"):
        """Add a new post to tracking"""
        post = {
            "id": len(self.posts) + 1,
            "subreddit": subreddit,
            "title": title,
            "url": url,
            "post_type": post_type,  # "main" or "comment"
            "posted_at": datetime.now().isoformat(),
            "last_checked": None,
            "upvotes": 0,
            "comments": 0,
            "status": "active",  # "active", "removed", "deleted"
            "notes": ""
        }

        self.posts.append(post)
        self.save_posts()

        print(f"✅ Added post to tracking:")
        print(f"   Subreddit: r/{subreddit}")
        print(f"   Title: {title[:50]}...")
        print(f"   URL: {url}")

    def update_metrics(self, post_id: int, upvotes: int, comments: int, status: str = "active"):
        """Update post metrics"""
        for post in self.posts:
            if post["id"] == post_id:
                post["upvotes"] = upvotes
                post["comments"] = comments
                post["status"] = status
                post["last_checked"] = datetime.now().isoformat()
                break

        self.save_posts()

    def add_note(self, post_id: int, note: str):
        """Add note to post"""
        for post in self.posts:
            if post["id"] == post_id:
                if post["notes"]:
                    post["notes"] += f" | {note}"
                else:
                    post["notes"] = note
                break

        self.save_posts()

    def export_csv(self):
        """Export tracking data to CSV"""
        if not self.posts:
            print("⚠️ No posts to export")
            return

        fieldnames = [
            "id", "subreddit", "title", "url", "post_type",
            "posted_at", "last_checked", "upvotes", "comments",
            "status", "notes"
        ]

        with open(self.csv_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.posts)

        print(f"✅ Exported to: {self.csv_file}")

    def generate_report(self) -> str:
        """Generate markdown report"""
        report = f"# Post Tracking Report\n\n"
        report += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        report += f"**Total Posts**: {len(self.posts)}\n\n"

        # Summary stats
        active = sum(1 for p in self.posts if p["status"] == "active")
        removed = sum(1 for p in self.posts if p["status"] == "removed")
        total_upvotes = sum(p["upvotes"] for p in self.posts)
        total_comments = sum(p["comments"] for p in self.posts)

        report += f"## Summary\n\n"
        report += f"- Active posts: {active}\n"
        report += f"- Removed posts: {removed}\n"
        report += f"- Total upvotes: {total_upvotes}\n"
        report += f"- Total comments: {total_comments}\n\n"

        # Per-post details
        report += f"## Post Details\n\n"

        for post in self.posts:
            status_icon = "✅" if post["status"] == "active" else "❌"
            report += f"### {status_icon} [{post['id']}] r/{post['subreddit']}\n\n"
            report += f"**Title**: {post['title']}\n\n"
            report += f"**URL**: {post['url']}\n\n"
            report += f"**Metrics**:\n"
            report += f"- Upvotes: {post['upvotes']}\n"
            report += f"- Comments: {post['comments']}\n"
            report += f"- Status: {post['status']}\n\n"

            if post['notes']:
                report += f"**Notes**: {post['notes']}\n\n"

            report += "---\n\n"

        return report

    def print_summary(self):
        """Print tracking summary to console"""
        print("\n" + "="*60)
        print("POST TRACKING SUMMARY")
        print("="*60 + "\n")

        for post in self.posts:
            status = "✅" if post["status"] == "active" else "❌"
            print(f"{status} [{post['id']}] r/{post['subreddit']}")
            print(f"    Title: {post['title'][:50]}...")
            print(f"    Upvotes: {post['upvotes']} | Comments: {post['comments']}")
            print(f"    URL: {post['url']}")
            if post['notes']:
                print(f"    Notes: {post['notes']}")
            print()

def main():
    """Main execution flow"""
    tracker = PostTracker(output_dir=".")

    # Example usage
    print("📊 Reddit Post Tracker\n")
    print("Commands:")
    print("  1. Add new post")
    print("  2. Update metrics")
    print("  3. Add note")
    print("  4. Generate report")
    print("  5. Export CSV")
    print("  6. Show summary")
    print("  0. Exit\n")

    while True:
        choice = input("Enter command (0-6): ").strip()

        if choice == "1":
            subreddit = input("Subreddit (without r/): ").strip()
            title = input("Post title: ").strip()
            url = input("Post URL: ").strip()
            post_type = input("Type (main/comment) [main]: ").strip() or "main"
            tracker.add_post(subreddit, title, url, post_type)

        elif choice == "2":
            post_id = int(input("Post ID: ").strip())
            upvotes = int(input("Upvotes: ").strip())
            comments = int(input("Comments: ").strip())
            status = input("Status (active/removed) [active]: ").strip() or "active"
            tracker.update_metrics(post_id, upvotes, comments, status)
            print("✅ Metrics updated")

        elif choice == "3":
            post_id = int(input("Post ID: ").strip())
            note = input("Note: ").strip()
            tracker.add_note(post_id, note)
            print("✅ Note added")

        elif choice == "4":
            report = tracker.generate_report()
            report_file = f"tracking_report_{datetime.now().strftime('%Y%m%d')}.md"
            with open(report_file, "w") as f:
                f.write(report)
            print(f"✅ Report saved to: {report_file}")

        elif choice == "5":
            tracker.export_csv()

        elif choice == "6":
            tracker.print_summary()

        elif choice == "0":
            print("👋 Goodbye!")
            break

        else:
            print("⚠️ Invalid command")

        print()

if __name__ == "__main__":
    main()
