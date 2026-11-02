<!--
  The cover page every document opens with. build_deliverables.py puts it at
  the front of each one and fills in two placeholders:

      {{TITLE}}     the course name, the same on all three covers. It comes
                    from COVER_TITLE in build_deliverables.py.
      {{SUBTITLE}}  what this particular document is - "Participant
                    Reference Manual", "Trainer Manual", "Running Order".
                    It comes from the document's own row in DOCUMENTS, in
                    the same file, and is optional: give a document an empty
                    subtitle and the line disappears from its cover rather
                    than leaving a gap.

      {{PUBLISHED}}  the day the PDF was built, as dd/mm/yyyy. It comes
                    from the build, not from any setting, so it is always
                    the date on the file rather than a date someone has to
                    remember to change. The words around it are ordinary
                    text here, so "Published date:" can be reworded or the
                    whole line deleted.

      {{CLIENT_LOGO}}  the client's logo, under Professional Training's own,
                    from client_logo in document_settings.toml. Also
                    optional, and also leaves nothing behind when unset:
                    the paragraph holding it goes with it. Its width is
                    fixed in the stylesheet as a share of the Professional
                    Training logo's, so the two always sit in proportion.

  Both are dropped into raw HTML, so a long title can be broken exactly
  where you want it with <br> - for example
  "AI in Excel Using ChatGPT &amp;amp; Copilot<br>Half Day". Nothing here
  wraps or splits a title on your behalf.

  Edit this file to change the branding on all three documents at once; it
  is not a document in its own right and is never exported on its own.

  Exporting a document from VS Code instead of running the build produces a
  PDF with no cover page, because nothing substitutes the placeholders.
-->

<div align="center" class="cover">

<br>

<h1 class="cover-title">{{TITLE}}</h1>

<br>

<hr style="border: none; border-top: 4px solid #000;">

<br>

<p style="font-size: 1.5em;">{{SUBTITLE}}</p>

<br>

<p class="cover-logo"><img src="assets/professional_logo.jpg" alt="professional.ie"></p>

<p class="client-logo">{{CLIENT_LOGO}}</p>

<br><br>

<p><strong>Cork:</strong> (021) 4319010 &nbsp;<strong>Dublin:</strong> (01) 6627700</p>
<p><strong>Limerick:</strong> (061) 311982</p>
<p><strong>Website:</strong> <a href="https://www.professional.ie">www.professional.ie</a></p>
<p><strong>E Mail:</strong> <a href="mailto:info@professional.ie">info@professional.ie</a></p>

<br>

<hr style="border: none; border-top: 1px solid #888;">

<p class="published">Published date: {{PUBLISHED}}</p>

</div>
