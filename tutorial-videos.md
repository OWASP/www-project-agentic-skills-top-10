---
layout: col-sidebar
title: Tutorial Videos
tags: agentic-security, tutorials, video
level: 2
type: documentation
description: "Tutorial videos for the OWASP Agentic Skills Top 10."
permalink: /videos/
---

<style>
  .ast-video-page {
    color: #172033;
  }

  .ast-video-hero {
    padding: 22px 0 18px;
    border-bottom: 1px solid #d8dee9;
    margin-bottom: 22px;
  }

  .ast-video-kicker {
    margin: 0 0 6px;
    color: #a44300;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .ast-video-hero h1 {
    margin: 0 0 10px;
    color: #101827;
    font-size: clamp(2rem, 4vw, 3.35rem);
    line-height: 1.04;
  }

  .ast-video-hero p {
    max-width: 860px;
    margin: 0;
    color: #40516c;
    font-size: 1.04rem;
    line-height: 1.6;
  }

  .ast-video-player-panel {
    border: 1px solid #d8dee9;
    border-radius: 8px;
    background: #ffffff;
    box-shadow: 0 10px 28px rgba(16, 24, 39, 0.08);
    overflow: hidden;
    margin-bottom: 28px;
  }

  .ast-video-player-wrap {
    background: #0f172a;
  }

  .ast-video-player {
    display: block;
    width: 100%;
    aspect-ratio: 16 / 9;
    background: #0f172a;
  }

  .ast-video-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 18px 20px;
    border-top: 1px solid #d8dee9;
  }

  .ast-video-meta h2 {
    margin: 0 0 4px;
    color: #101827;
    font-size: 1.35rem;
    line-height: 1.25;
  }

  .ast-video-meta p {
    margin: 0;
    color: #51627e;
    line-height: 1.55;
  }

  .ast-video-direct-link {
    flex: 0 0 auto;
    border: 1px solid #bf4b00;
    border-radius: 999px;
    padding: 9px 14px;
    color: #8f3500;
    font-weight: 700;
    text-decoration: none;
    white-space: nowrap;
  }

  .ast-video-direct-link:hover {
    background: #fff4eb;
    color: #662600;
    text-decoration: none;
  }

  .ast-video-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 16px;
    margin: 0 0 32px;
  }

  .ast-video-card {
    display: flex;
    flex-direction: column;
    min-height: 100%;
    border: 1px solid #d8dee9;
    border-radius: 8px;
    background: #ffffff;
    color: inherit;
    overflow: hidden;
    text-decoration: none;
    transition: border-color 0.15s ease, box-shadow 0.15s ease, transform 0.15s ease;
  }

  .ast-video-card:hover,
  .ast-video-card:focus {
    border-color: #bf4b00;
    box-shadow: 0 10px 24px rgba(16, 24, 39, 0.12);
    text-decoration: none;
    transform: translateY(-1px);
  }

  .ast-video-card[aria-current="true"] {
    border-color: #bf4b00;
    box-shadow: 0 0 0 3px rgba(191, 75, 0, 0.15);
  }

  .ast-video-thumb {
    display: block;
    width: 100%;
    aspect-ratio: 16 / 9;
    object-fit: cover;
    background: #eef2f7;
    border-bottom: 1px solid #d8dee9;
  }

  .ast-video-card-body {
    display: flex;
    flex-direction: column;
    gap: 8px;
    padding: 14px;
  }

  .ast-video-card-id {
    color: #9a3a00;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.07em;
    text-transform: uppercase;
  }

  .ast-video-card-title {
    color: #101827;
    font-size: 1.02rem;
    font-weight: 800;
    line-height: 1.25;
  }

  .ast-video-card-copy {
    color: #51627e;
    font-size: 0.9rem;
    line-height: 1.45;
  }

  .ast-video-play-label {
    margin-top: auto;
    color: #8f3500;
    font-size: 0.88rem;
    font-weight: 800;
  }

  .ast-video-note {
    border-left: 4px solid #bf4b00;
    padding: 12px 16px;
    background: #fff7ef;
    color: #4d3b2d;
    line-height: 1.55;
  }

  @media (max-width: 720px) {
    .ast-video-meta {
      align-items: flex-start;
      flex-direction: column;
    }

    .ast-video-direct-link {
      white-space: normal;
    }
  }
</style>

<div class="ast-video-page">
  <section class="ast-video-hero" aria-labelledby="ast-video-title">
    <p class="ast-video-kicker">OWASP Agentic Skills Top 10</p>
    <h1 id="ast-video-title">Tutorial Videos</h1>
    <p>Use these short tutorials to introduce each AST risk, explain the main security concern, and guide reviewers or teams through the corresponding mitigation mindset. Select a card below to play a video, or share a direct link using the <code>?video=ast01</code> through <code>?video=ast10</code> URL parameter.</p>
  </section>

  <section class="ast-video-player-panel" aria-label="Selected tutorial video">
    <div class="ast-video-player-wrap">
      <video
        id="ast-video-player"
        class="ast-video-player"
        controls
        preload="metadata"
        poster="/www-project-agentic-skills-top-10/assets/images/video-posters/ast01.png">
        <source id="ast-video-source" src="/www-project-agentic-skills-top-10/assets/videos/ast01-malicious-skills.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>
    <div class="ast-video-meta">
      <div>
        <h2 id="ast-video-current-title">AST01: Malicious Skills</h2>
        <p id="ast-video-current-copy">Malicious skills may appear legitimate while embedding harmful behavior that can compromise agent execution and trust.</p>
      </div>
      <a id="ast-video-current-link" class="ast-video-direct-link" href="/www-project-agentic-skills-top-10/videos?video=ast01">Direct link</a>
    </div>
  </section>

  <section aria-labelledby="ast-video-library-title">
    <h2 id="ast-video-library-title">Select A Tutorial</h2>
    <div class="ast-video-grid">
      <a class="ast-video-card" href="/www-project-agentic-skills-top-10/videos?video=ast01" data-video-id="ast01" aria-current="true">
        <img class="ast-video-thumb" src="/www-project-agentic-skills-top-10/assets/images/video-posters/ast01.png" alt="Poster for AST01 Malicious Skills tutorial">
        <span class="ast-video-card-body">
          <span class="ast-video-card-id">AST01</span>
          <span class="ast-video-card-title">Malicious Skills</span>
          <span class="ast-video-card-copy">Skills that look useful or legitimate but contain hidden malicious behavior.</span>
          <span class="ast-video-play-label">Play video</span>
        </span>
      </a>

      <a class="ast-video-card" href="/www-project-agentic-skills-top-10/videos?video=ast02" data-video-id="ast02">
        <img class="ast-video-thumb" src="/www-project-agentic-skills-top-10/assets/images/video-posters/ast02.png" alt="Poster for AST02 Supply Chain Compromise tutorial">
        <span class="ast-video-card-body">
          <span class="ast-video-card-id">AST02</span>
          <span class="ast-video-card-title">Supply Chain Compromise</span>
          <span class="ast-video-card-copy">Registry, dependency, or distribution weaknesses that let compromised skills reach users.</span>
          <span class="ast-video-play-label">Play video</span>
        </span>
      </a>

      <a class="ast-video-card" href="/www-project-agentic-skills-top-10/videos?video=ast03" data-video-id="ast03">
        <img class="ast-video-thumb" src="/www-project-agentic-skills-top-10/assets/images/video-posters/ast03.png" alt="Poster for AST03 Over-Privileged Skills tutorial">
        <span class="ast-video-card-body">
          <span class="ast-video-card-id">AST03</span>
          <span class="ast-video-card-title">Over-Privileged Skills</span>
          <span class="ast-video-card-copy">Skills granted broader permissions than their purpose requires.</span>
          <span class="ast-video-play-label">Play video</span>
        </span>
      </a>

      <a class="ast-video-card" href="/www-project-agentic-skills-top-10/videos?video=ast04" data-video-id="ast04">
        <img class="ast-video-thumb" src="/www-project-agentic-skills-top-10/assets/images/video-posters/ast04.png" alt="Poster for AST04 Insecure Metadata tutorial">
        <span class="ast-video-card-body">
          <span class="ast-video-card-id">AST04</span>
          <span class="ast-video-card-title">Insecure Metadata</span>
          <span class="ast-video-card-copy">Missing, misleading, or weak metadata that breaks review and trust decisions.</span>
          <span class="ast-video-play-label">Play video</span>
        </span>
      </a>

      <a class="ast-video-card" href="/www-project-agentic-skills-top-10/videos?video=ast05" data-video-id="ast05">
        <img class="ast-video-thumb" src="/www-project-agentic-skills-top-10/assets/images/video-posters/ast05.png" alt="Poster for AST05 Untrusted External Instructions tutorial">
        <span class="ast-video-card-body">
          <span class="ast-video-card-id">AST05</span>
          <span class="ast-video-card-title">Untrusted External Instructions</span>
          <span class="ast-video-card-copy">External content that reshapes skill behavior or overrides the intended task.</span>
          <span class="ast-video-play-label">Play video</span>
        </span>
      </a>

      <a class="ast-video-card" href="/www-project-agentic-skills-top-10/videos?video=ast06" data-video-id="ast06">
        <img class="ast-video-thumb" src="/www-project-agentic-skills-top-10/assets/images/video-posters/ast06.png" alt="Poster for AST06 Weak Isolation tutorial">
        <span class="ast-video-card-body">
          <span class="ast-video-card-id">AST06</span>
          <span class="ast-video-card-title">Weak Isolation</span>
          <span class="ast-video-card-copy">Skills that execute with inadequate sandboxing, boundaries, or containment.</span>
          <span class="ast-video-play-label">Play video</span>
        </span>
      </a>

      <a class="ast-video-card" href="/www-project-agentic-skills-top-10/videos?video=ast07" data-video-id="ast07">
        <img class="ast-video-thumb" src="/www-project-agentic-skills-top-10/assets/images/video-posters/ast07.png" alt="Poster for AST07 Update Drift tutorial">
        <span class="ast-video-card-body">
          <span class="ast-video-card-id">AST07</span>
          <span class="ast-video-card-title">Update Drift</span>
          <span class="ast-video-card-copy">Behavior, dependency, or configuration changes that alter risk after approval.</span>
          <span class="ast-video-play-label">Play video</span>
        </span>
      </a>

      <a class="ast-video-card" href="/www-project-agentic-skills-top-10/videos?video=ast08" data-video-id="ast08">
        <img class="ast-video-thumb" src="/www-project-agentic-skills-top-10/assets/images/video-posters/ast08.png" alt="Poster for AST08 Poor Scanning tutorial">
        <span class="ast-video-card-body">
          <span class="ast-video-card-id">AST08</span>
          <span class="ast-video-card-title">Poor Scanning</span>
          <span class="ast-video-card-copy">Insufficient review, detection, or validation before skills enter real workflows.</span>
          <span class="ast-video-play-label">Play video</span>
        </span>
      </a>

      <a class="ast-video-card" href="/www-project-agentic-skills-top-10/videos?video=ast09" data-video-id="ast09">
        <img class="ast-video-thumb" src="/www-project-agentic-skills-top-10/assets/images/video-posters/ast09.png" alt="Poster for AST09 No Governance tutorial">
        <span class="ast-video-card-body">
          <span class="ast-video-card-id">AST09</span>
          <span class="ast-video-card-title">No Governance</span>
          <span class="ast-video-card-copy">Lack of inventory, ownership, policy, review, and incident response for skills.</span>
          <span class="ast-video-play-label">Play video</span>
        </span>
      </a>

      <a class="ast-video-card" href="/www-project-agentic-skills-top-10/videos?video=ast10" data-video-id="ast10">
        <img class="ast-video-thumb" src="/www-project-agentic-skills-top-10/assets/images/video-posters/ast10.png" alt="Poster for AST10 Cross-Platform Reuse tutorial">
        <span class="ast-video-card-body">
          <span class="ast-video-card-id">AST10</span>
          <span class="ast-video-card-title">Cross-Platform Reuse</span>
          <span class="ast-video-card-copy">Moving skills across platforms without preserving source security assumptions.</span>
          <span class="ast-video-play-label">Play video</span>
        </span>
      </a>
    </div>
  </section>

  <p class="ast-video-note">Direct access format: <code>/www-project-agentic-skills-top-10/videos?video=ast01</code>. Replace <code>ast01</code> with any item from <code>ast02</code> through <code>ast10</code>.</p>
</div>

<script>
  (function () {
    var basePath = "/www-project-agentic-skills-top-10";
    var videos = {
      ast01: {
        title: "AST01: Malicious Skills",
        copy: "Malicious skills may appear legitimate while embedding harmful behavior that can compromise agent execution and trust.",
        file: "ast01-malicious-skills.mp4",
        poster: "ast01.png"
      },
      ast02: {
        title: "AST02: Supply Chain Compromise",
        copy: "Registry and distribution weaknesses can let compromised or unverified skills reach agent users.",
        file: "ast02-supply-chain-compromise.mp4",
        poster: "ast02.png"
      },
      ast03: {
        title: "AST03: Over-Privileged Skills",
        copy: "Excessive permissions turn ordinary skill behavior into a path for unauthorized access or impact.",
        file: "ast03-over-privileged-skills.mp4",
        poster: "ast03.png"
      },
      ast04: {
        title: "AST04: Insecure Metadata",
        copy: "Weak or misleading metadata undermines security review, provenance, and informed trust decisions.",
        file: "ast04-insecure-metadata.mp4",
        poster: "ast04.png"
      },
      ast05: {
        title: "AST05: Untrusted External Instructions",
        copy: "External content can inject instructions that redirect the skill away from the user intent.",
        file: "ast05-untrusted-external-instructions.mp4",
        poster: "ast05.png"
      },
      ast06: {
        title: "AST06: Weak Isolation",
        copy: "Insufficient containment lets a skill affect files, tools, networks, or processes outside its intended boundary.",
        file: "ast06-weak-isolation.mp4",
        poster: "ast06.png"
      },
      ast07: {
        title: "AST07: Update Drift",
        copy: "Post-approval changes can quietly alter skill behavior, dependencies, permissions, or risk.",
        file: "ast07-update-drift.mp4",
        poster: "ast07.png"
      },
      ast08: {
        title: "AST08: Poor Scanning",
        copy: "Skills need effective scanning and review before they are trusted in real agent workflows.",
        file: "ast08-poor-scanning.mp4",
        poster: "ast08.png"
      },
      ast09: {
        title: "AST09: No Governance",
        copy: "Without ownership, inventory, policy, and response, skill risk becomes invisible until an incident occurs.",
        file: "ast09-no-governance.mp4",
        poster: "ast09.png"
      },
      ast10: {
        title: "AST10: Cross-Platform Reuse",
        copy: "A skill moved between platforms can lose the security assumptions and metadata that made it safe.",
        file: "ast10-cross-platform-reuse.mp4",
        poster: "ast10.png"
      }
    };

    var player = document.getElementById("ast-video-player");
    var source = document.getElementById("ast-video-source");
    var title = document.getElementById("ast-video-current-title");
    var copy = document.getElementById("ast-video-current-copy");
    var directLink = document.getElementById("ast-video-current-link");
    var cards = Array.prototype.slice.call(document.querySelectorAll(".ast-video-card[data-video-id]"));

    function normalizeVideoId(value) {
      var id = String(value || "").trim().toLowerCase();
      return Object.prototype.hasOwnProperty.call(videos, id) ? id : "ast01";
    }

    function videoFromLocation() {
      var params = new URLSearchParams(window.location.search);
      return normalizeVideoId(params.get("video") || window.location.hash.replace("#", ""));
    }

    function setSelectedVideo(id, shouldPlay, shouldPushState) {
      var selectedId = normalizeVideoId(id);
      var video = videos[selectedId];
      var videoUrl = basePath + "/assets/videos/" + video.file;
      var posterUrl = basePath + "/assets/images/video-posters/" + video.poster;
      var pageUrl = basePath + "/videos?video=" + selectedId;

      if (source.getAttribute("src") !== videoUrl) {
        source.setAttribute("src", videoUrl);
        player.setAttribute("poster", posterUrl);
        player.load();
      }

      title.textContent = video.title;
      copy.textContent = video.copy;
      directLink.setAttribute("href", pageUrl);

      cards.forEach(function (card) {
        var isSelected = card.getAttribute("data-video-id") === selectedId;
        card.setAttribute("aria-current", isSelected ? "true" : "false");
      });

      if (shouldPushState) {
        window.history.pushState({ video: selectedId }, "", pageUrl);
      }

      if (shouldPlay) {
        player.play().catch(function () {
          player.focus();
        });
      }
    }

    cards.forEach(function (card) {
      card.addEventListener("click", function (event) {
        event.preventDefault();
        setSelectedVideo(card.getAttribute("data-video-id"), true, true);
      });
    });

    window.addEventListener("popstate", function () {
      setSelectedVideo(videoFromLocation(), false, false);
    });

    setSelectedVideo(videoFromLocation(), false, false);
  })();
</script>
