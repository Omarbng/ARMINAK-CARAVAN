# attic

Work that is no longer shipped but was not worth destroying.

## dunes.js

A raymarched dune landscape (WebGL, ~12 KB), written as scaffolding for the
drawn hero — it rendered the terrain the SVG caravan stood on. The client asked
for real footage instead ("настоящая графика"), so the hero became a rendered
film and this became orphaned: no page loaded it, and `dunes.html` carries its
own inline shader rather than using this file.

Kept because it was never committed to git — deleting it would have been the
only copy. Nothing references it; restoring means moving it back to
`site/assets/js/` and adding a `<script>` tag.
