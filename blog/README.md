# Monkey Mart Blog

This is the Jekyll-based blog for the Monkey Mart gaming website. This README provides instructions for maintaining and updating the blog.

## Table of Contents
- [Setup](#setup)
- [Creating New Posts](#creating-new-posts)
- [Adding Images](#adding-images)
- [Publishing with GitHub Pages](#publishing)
- [SEO Guidelines](#seo-guidelines)
- [Troubleshooting](#troubleshooting)

## Setup

### Option 3: Direct GitHub Pages Publishing (No Local Installation Required)
This is the recommended approach if you don't want to install Ruby and Jekyll locally.

1. **Create a GitHub Repository**
   - Push your blog files to a GitHub repository
   - Name the repository according to your preference (e.g., `monkey-mart-blog`)

2. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Navigate to Settings > Pages
   - Select the branch you want to publish from (usually `main`)
   - Choose the `/docs` folder or root folder as your publishing source
   - Save your changes

3. **Configure Custom Domain** (Optional)
   - In the GitHub Pages settings, enter your custom domain (e.g., monkeymart.one/blog)
   - Update your DNS records to point to GitHub Pages
   - Add a CNAME file to your repository with your domain name

### Creating New Posts

To create a new blog post:

1. Create a new file in the `_posts` directory with the naming format: `YYYY-MM-DD-title-of-post.md`
2. At the top of the file, include the front matter block:
   ```
   ---
   layout: post
   title: "Your Post Title"
   date: YYYY-MM-DD
   categories: [category1, category2]
   tags: [tag1, tag2, tag3]
   image: /img/blog/your-image.jpg
   description: "A brief description of your post for SEO."
   author: "Your Name"
   ---
   ```
3. Write your post content below the front matter using Markdown
4. Commit and push your changes to GitHub

### Adding Images

1. Place your images in the `img/blog/` directory
2. Reference them in your posts using: `![Alt text](/img/blog/your-image.jpg)`
3. For featured images, add the path to the `image` field in the front matter

### Publishing with GitHub Pages

When you're ready to publish:

1. Commit and push your changes to the GitHub repository
2. GitHub will automatically build and deploy your site
3. Your changes will be live within a few minutes
4. Check the Actions tab in your repository to monitor the build process

If you want to check your site before publishing:
- You can use GitHub's preview feature by clicking on the deployment in the "Environments" section of your repository
- Each pull request also generates a preview deployment you can review

### SEO Guidelines

For better search engine visibility:

1. Use descriptive titles with your target keywords
2. Include a meta description for each post
3. Use headings (H1, H2, H3) properly
4. Add alt text to all images
5. Include internal links to other posts
6. Use categories and tags consistently

### Troubleshooting

Common issues and solutions:

1. **Site not building:**
   - Check the build logs in GitHub Actions
   - Make sure your files use proper Markdown syntax
   - Check for YAML formatting errors in front matter

2. **Images not displaying:**
   - Verify the file paths are correct
   - Ensure images are pushed to the correct directory
   - Check case sensitivity in file names and paths

3. **Custom domain issues:**
   - Verify DNS settings are correctly configured
   - Ensure your CNAME file is properly set up
   - Give DNS changes up to 48 hours to propagate

---

## Appendix: Useful Resources

- [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Liquid Template Language](https://shopify.github.io/liquid/) 