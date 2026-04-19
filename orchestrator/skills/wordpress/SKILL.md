# WordPress Blog Skill

Use this skill to publish blog posts to WordPress sites via REST API.

## When to Use
- User asks to "write a blog", "publish post", "create article"
- User mentions WordPress, WP, blog posts, articles
- User wants to create content for a website

## Actions
1. Use WordPress REST API: `POST /wp-json/wp/v2/posts`
2. Requires: site_url, username, application_password
3. Create draft or publish directly

## Parameters
- title: Post title
- content: Post content (HTML or markdown)
- status: "draft" | "publish"
- categories: list of category IDs
- tags: list of tag IDs
