---
layout: post
title: Your AI Built a Beautiful House, but nobody Locked the door.
categories:
  - VibeCoding
  - Security
excerpt: Oh boy.. This will be a long one.
image: /assets/images/lock_the_door.png
date: 2026-03-23
read_time: 10
---

## Introduction

Imagine you've just built your dream app. No coding bootcamp, no computer science degree, no idea what a database even is - just you, an AI, and the unshakeable belief that this time next year you'll be on a yacht. You've got real users, real signups, maybe even some press coverage calling you a "disruptor." Life is good. The hustle is real.

Now imagine waking up to find that every profile photo, every verification selfie, every government ID your users ever trusted you with - all 72,000 of them - has been sitting in a publicly accessible bucket. No password. No authentication. No nothing. Just "vibing" there on the internet, free for anyone who bothered to look. Like leaving your diary on a park bench and being surprised someone read it.

That's not a hypothetical. That's Tea App. A women-only dating safety app - _safety_ app, let that one sink in - whose founder admitted he didn't know how to code. The AI built it. The AI shipped it. And somewhere in that process, nobody - not the founder nor the AI stopped to ask "hey, where exactly are we putting all these government IDs people are sending us, and who can see them?"

The breach exposed 13,000 government ID photos. Real names. Real faces. Real passports and driver's licenses. Nearly a dozen lawsuits followed - which is a fun way to find out your MVP has "some" issues.

The security researcher who discovered it didn't need to be some elite hacker working from a dimly lit basement. The storage bucket had _zero_ authentication. His verdict was almost impressive in its simplicity: _"No authentication, no nothing. It's a public bucket."_

Here's the uncomfortable truth nobody puts in their "I built a SaaS in a weekend" Twitter thread: the AI did exactly what it was asked. It built something that _worked_. It just didn't build something that was _safe_ - because you never asked it to, and you wouldn't have known to.

## Vibe Coding has come to stay

There is no doubt. Vibe coding has come to stay, for better and for worse. I've seen people create incredible projects with real value, but I've also seen the _hustlers_. That's the name I give them, the _Hustlers_. They are the people that have absolutely no IT experience whatsoever, barely know where the settings on a laptop are, that have now discovered AI coding tools. They see it as their ticket to paradise, this is how they're going to make it big!

In fairness, there's nothing wrong with being a _Hustler_. Being focused and creative, and wanting to build something for yourself is great! However... Not giving a single thought to security whilst building that something? Not so great. That's a fast track to becoming the next cautionary tale on a security blog.

Don't get me wrong - I'm not a developer in any way, and I'm a frequent user of Claude Code, working as a Cyber Security Engineer by day. I absolutely love it! In truth, I'm not here to trash talk people building their dreams. But I want to drive the point home. Vibe coding an app without any security focus will always equal trouble down the line. Maintenance will be hard or impossible if you have no connection to the code, bugs will be hard to fix, and security will be at rock bottom.

In most cases.

Please... Don't become the next Tea App.

## What the AI doesn't tell you 

Here's the thing about AI coding tools - they are incredibly good at their job. You describe what you want, and they build it. Fast, clean, and it actually works. Well, most of the time... That part is genuinely impressive and I'll never take that away from them.

But there's a catch nobody puts in the marketing material.

The AI doesn't know what you're building. Not really. It knows what you _told_ it - "build me a login page," "add a file upload feature," "let users store their profile photos." It takes that instruction, reaches into its vast knowledge of existing code, and produces something functional. What it doesn't do is stop and think _"hang on, this app is collecting government IDs from real people - maybe I should make sure nobody unauthorized can access those."_

That's not a flaw. That's just how it works. The AI is optimized for one thing: making code that runs. Security requires context - who are your users? What data are you handling? Who shouldn't have access, and what happens if they get it anyway? The AI has no idea, because you never told it. And if you don't know to ask, it won't volunteer the information.

This is how you end up with a storage bucket full of government IDs and zero authentication. Not because the AI made a mistake. Not because you're stupid. But because you asked it to build a house, and it built a beautiful house - but neither of you thought to put a lock on the door.

The good news? The same tool that built the house can absolutely help you lock it. You just have to know what to ask.

## Ask the right questions, get the right answers

Remember what we just established - the AI builds what you ask for. So let's start asking better questions. Before you ship anything, run through these. Copy them, paste them, use them. Your users will thank you, even if they never know why.

---

**1. The "try to break it" prompt**

Most people ask Claude to build features. Almost nobody asks Claude to attack them. Flipping that switch is the single biggest thing you can do before shipping.

**What you're protecting against:** Attackers don't use your app the way you intended. They poke, prod, and send unexpected inputs to see what breaks - and what leaks.

Drop this into Claude after building any feature:

<div class="prompt-box">
"You are a malicious attacker trying to abuse this application. Review this code and tell me every way you could exploit it, extract data, bypass authentication, or cause it to behave in unintended ways. Be specific."_
</div>
---

**2. The "what are you storing and why" prompt**

The Tea App problem in a nutshell - data was being collected and stored without anyone really thinking about what that meant. The less data you store, the less you can leak.

**What you're protecting against:** Storing sensitive data you don't need, in places you haven't secured, in formats that are easy to exploit.

<div class="prompt-box">
"Review this code and list every piece of user data being collected or stored. For each one, tell me: is this necessary, where is it stored, who can access it, and is it being stored securely? Flag anything that looks risky."_
</div>
---

**3. The "who can see what" prompt**

Authentication is whether you can log in. Authorisation is whether you should be allowed to see what you're looking at after you log in. Most vibe coders think about the first one and completely forget the second.

**What you're protecting against:** Users accessing other users' data, regular users accessing admin features, or - like Tea App, unauthenticated users accessing everything.

<div class="prompt-box">
"Review this code and check every endpoint, function, and data access point. For each one, tell me who is allowed to access it and whether that restriction is actually enforced in the code. Flag anywhere that access control is missing, weak, or could be bypassed."_
</div>
---

**4. The "find the secrets" prompt**

AI generated code has a charming habit of hardcoding API keys, passwords, and credentials directly into your code. You push it to GitHub, GitHub is public, and within minutes automated bots have found and are using your credentials. This one is almost a rite of passage at this point.

**What you're protecting against:** Exposed API keys, database passwords, and credentials ending up somewhere they shouldn't - like a public repository.

<div class="prompt-box">
"Scan this code for any hardcoded secrets, API keys, passwords, tokens, or credentials. Also tell me if there are any places where sensitive configuration values should be moved to environment variables but haven't been."_
</div>
---

**5. The pre-ship checklist prompt**

This is your safety net. Run this on your entire codebase before you go live. Think of it as the lock-check before you leave the house.

<div class="prompt-box">
"You are a senior security engineer doing a final review before this application goes to production. Check for: hardcoded secrets, missing authentication or authorisation, exposed sensitive data, SQL injection vulnerabilities, insecure file storage, missing input validation, and any insecure default configurations. For every issue you find, explain what could go wrong in plain English and tell me how to fix it."_
</div>
---

None of these prompts require you to understand security deeply. You just need to understand the answers well enough to act on them - and if something Claude flags sounds scary, that's because it probably is.

## Go build something. Just lock the door first.

Vibe coding isn't going anywhere. The _Hustlers_ aren't going anywhere. And honestly? Neither are the security researchers who will gladly pick apart whatever gets shipped without a second thought. It's basically a food chain at this point.

The difference between the next Tea App and the next great indie success story isn't talent, funding, or even luck. It's whether someone stopped for twenty minutes before hitting deploy and asked Claude or any other AI for that matter, to try to break what they just built.

That's it. Twenty minutes. The time it takes to finish your white Monster Ultra and watch a YouTube video you'll forget by tomorrow. Except this time, instead of forgetting it, you'll have a list of things that could have ended your app, your reputation, and potentially landed you in legal trouble.

Not a great origin story.

So here's what I'm asking: take the prompts from this post, run them on whatever you're building, and see what comes back. Then come back here and tell me about it - send me an email or find me online on LinkedIn. I genuinely want to know what you find. Partly because it's useful feedback. Mostly because the results are usually either reassuring or absolutely terrifying, and either way it makes for a great story.

And if this post saved your app, or your users from becoming the next cautionary tale on a security blog, share it with the next _Hustler_ you know. They probably need it more than they realize.

Just don't tell them I called them a _Hustler_.
