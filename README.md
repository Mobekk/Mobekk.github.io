# Security Blog - GitHub Pages Setup

A minimal, professional blog for documenting security research, automation, and technical findings.

## 🚀 Quick Start - Test Locally

1. **Download these files** to your computer
2. **Open `index.html`** in your web browser
3. That's it! You should see your blog.

## 📝 How to Add a New Blog Post

### Step 1: Copy the Template
1. Go to the `posts/` folder
2. Copy `post-template.html`
3. Rename it (e.g., `my-new-post.html`)

### Step 2: Edit Your Post
Open your new file and update these sections:

```html
<!-- Line 6: Update the title -->
<title>Your Post Title Here - Security Blog</title>

<!-- Line 30-31: Update date and read time -->
<time>2026-01-21</time>
<span class="read-time">5 min read</span>

<!-- Line 33: Update the post title -->
<h1 class="post-title">Your Post Title Here</h1>

<!-- Lines 35-38: Update tags -->
<div class="tags">
    <span class="tag tag-dfir">dfir</span>
    <span class="tag tag-automation">automation</span>
</div>
```

**Available tag styles:**
- `tag-dfir` (red)
- `tag-automation` (green)
- `tag-python` (cyan)
- `tag-cloud` (yellow)
- `tag-aws` (orange)
- `tag-threat` (red)

### Step 3: Write Your Content
Replace the example content (starting at line 44) with your own. You can use:

**Headings:**
```html
<h2>Main Section</h2>
<h3>Subsection</h3>
```

**Paragraphs:**
```html
<p>Your text here.</p>
```

**Code blocks:**
```html
<pre><code>def my_function():
    return "Hello, World!"</code></pre>
```

**Lists:**
```html
<ul>
    <li>Bullet point</li>
    <li>Another point</li>
</ul>
```

**Links:**
```html
<a href="https://example.com">link text</a>
```

### Step 4: Add to Homepage
Edit `index.html` and add a new post card in the `<section class="posts-grid">` section:

```html
<article class="post-card">
    <div class="post-meta">
        <time>2026-01-21</time>
        <span class="separator">//</span>
        <span class="read-time">5 min read</span>
    </div>
    <h2><a href="posts/my-new-post.html">Your Post Title</a></h2>
    <p class="excerpt">
        A brief description of what this post is about.
    </p>
    <div class="tags">
        <span class="tag tag-dfir">dfir</span>
    </div>
</article>
```

## 🌐 Publishing to GitHub Pages

### Option 1: Using GitHub Website (Easiest)

1. **Create a GitHub account** (if you don't have one)
2. **Create a new repository** named `yourusername.github.io`
   - Example: If your username is `john-doe`, name it `john-doe.github.io`
3. **Upload files:**
   - Click "Add file" → "Upload files"
   - Drag all your blog files into the upload area
   - Click "Commit changes"
4. **Wait 1-2 minutes** for GitHub to build your site
5. **Visit** `https://yourusername.github.io` to see your live blog!

### Option 2: Using Git (If You Know Git)

```bash
# Initialize git in your blog folder
git init

# Add all files
git add .

# Commit
git commit -m "Initial blog setup"

# Add your GitHub repo as remote
git remote add origin https://github.com/yourusername/yourusername.github.io.git

# Push to GitHub
git push -u origin main
```

Your site will be live at `https://yourusername.github.io`

## 🔧 Customization

### Change Your Name and Links
Search for these placeholders and replace them:
- `[Your Name]` - Your actual name
- `yourusername` - Your GitHub username
- `yourprofile` - Your LinkedIn profile
- `your.email@example.com` - Your email

These appear in:
- `index.html` (footer)
- `about.html` (multiple places)
- All post files (footer)

### Change the Blog Name
In the header of each file, find:
```html
<span class="logo-text">security.blog</span>
```
Replace `security.blog` with your chosen name (like `memleak` or `rootcause`)

### Add More Tag Colors
In `css/style.css`, find the `.tag-` section and add new colors:
```css
.tag-yourname {
    border-color: #ff00ff;
    color: #ff00ff;
}
```

## 🎨 Design Notes

This blog uses a **terminal/cyberpunk aesthetic**:
- Dark background (#0a0e14)
- Monospace font (JetBrains Mono) for code/navigation
- Clean sans-serif (Archivo) for body text
- Accent colors: cyan, green, red, yellow
- Subtle grain texture overlay
- Smooth animations

## 🔗 Adding a Custom Domain

Once you've bought a domain (like `memleak.io`):

1. **In your blog folder**, create a file named `CNAME` (no extension)
2. **Inside CNAME**, put just your domain:
   ```
   memleak.io
   ```
3. **In your domain registrar** (Namecheap, Cloudflare, etc.), add these DNS records:
   ```
   Type: A
   Host: @
   Value: 185.199.108.153
   
   Type: A
   Host: @
   Value: 185.199.109.153
   
   Type: A
   Host: @
   Value: 185.199.110.153
   
   Type: A
   Host: @
   Value: 185.199.111.153
   ```
4. **Wait 24 hours** for DNS to propagate

Now your blog will be at `yourdomain.com` instead of `username.github.io`!

## 📁 File Structure

```
your-blog/
├── index.html              # Homepage
├── about.html              # About page
├── README.md               # This file
├── CNAME                   # (Optional) Custom domain
├── css/
│   └── style.css           # All styling
└── posts/
    ├── example-dfir.html
    ├── example-cloud.html
    └── post-template.html  # Copy this for new posts
```

## ❓ Troubleshooting

**Blog doesn't load on GitHub Pages:**
- Make sure repository name is exactly `yourusername.github.io`
- Wait 2-5 minutes after pushing changes
- Check Settings → Pages to see if it's enabled

**Styles not loading:**
- Check that `css/style.css` path is correct
- For posts, use `../css/style.css` (note the `..`)

**Custom domain not working:**
- Wait 24-48 hours for DNS propagation
- Verify DNS records are correct
- Check CNAME file contains only your domain

## 🚀 Next Steps

1. Customize the placeholder text with your info
2. Write your first real post
3. Push to GitHub Pages
4. Share with the security community!

## 💡 Tips

- Keep posts focused and technical
- Include code examples when relevant
- Add tags to help readers find related content
- Update the homepage regularly with new posts
- Consider adding social media meta tags for better sharing

---

Good luck with your blog! 🔐
