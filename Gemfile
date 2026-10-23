source "https://rubygems.org"

# Build only the components this blog uses; github-pages pulls in unused plugins.
gem "jekyll", "~> 4.4"
gem "jekyll-feed", "~> 0.18", group: :jekyll_plugins
# Jekyll loads ERB explicitly on Ruby 3.4+.
gem "erb", ">= 6.0.4", "< 7"
gem "json", ">= 2.21.2", "< 3"

group :development do
  gem "bundler-audit", "~> 0.9", require: false
end
