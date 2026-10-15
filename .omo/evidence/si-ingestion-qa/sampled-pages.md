# SI Ingestion QA Sampled Page Checks

Sampled files:

- `wiki/factors/sun.md`
- `wiki/axes/sun-moon.md`
- `wiki/axes/jupiter-uranus.md`
- `wiki/activations/jupiter-uranus-equals-sun.md`
- `wiki/activations/sun-jupiter-equals-moon.md`
- `wiki/triads/sun-jupiter-uranus.md`

## Anchor Check

Invocation:

```powershell
Select-String -Path wiki/factors/sun.md,wiki/axes/sun-moon.md,wiki/axes/jupiter-uranus.md,wiki/activations/jupiter-uranus-equals-sun.md,wiki/activations/sun-jupiter-equals-moon.md -Pattern '<a id=\"derived-synthesis\"></a>'
```

Result: exit `0`.

Output:

```text
wiki\factors\sun.md:236:<a id="derived-synthesis"></a>
wiki\axes\sun-moon.md:332:<a id="derived-synthesis"></a>
wiki\axes\jupiter-uranus.md:267:<a id="derived-synthesis"></a>
wiki\activations\jupiter-uranus-equals-sun.md:94:<a id="derived-synthesis"></a>
wiki\activations\sun-jupiter-equals-moon.md:94:<a id="derived-synthesis"></a>
```

## Metadata And Orientation Check

Invocation:

```powershell
rg -n '<a id=\"derived-synthesis\"></a>|^## Derived Synthesis|^page_type:|^normalized_axis:|^normalized_formula:|^axis:|^activated_by:|^triad_set:|^orientations:|^  - (Jupiter/Uranus = Sun|Sun/Jupiter = Uranus|Sun/Uranus = Jupiter|Sun/Jupiter = Moon)' wiki/factors/sun.md wiki/axes/sun-moon.md wiki/axes/jupiter-uranus.md wiki/activations/jupiter-uranus-equals-sun.md wiki/activations/sun-jupiter-equals-moon.md wiki/triads/sun-jupiter-uranus.md
```

Result: exit `0`.

Relevant output:

```text
wiki/triads/sun-jupiter-uranus.md:3:page_type: triad_hub
wiki/triads/sun-jupiter-uranus.md:11:triad_set:
wiki/triads/sun-jupiter-uranus.md:15:orientations:
wiki/triads/sun-jupiter-uranus.md:16:  - Jupiter/Uranus = Sun
wiki/triads/sun-jupiter-uranus.md:17:  - Sun/Jupiter = Uranus
wiki/triads/sun-jupiter-uranus.md:18:  - Sun/Uranus = Jupiter
wiki/activations/jupiter-uranus-equals-sun.md:3:page_type: activation
wiki/activations/jupiter-uranus-equals-sun.md:11:normalized_formula: Jupiter/Uranus = Sun
wiki/activations/jupiter-uranus-equals-sun.md:12:axis: Jupiter/Uranus
wiki/activations/jupiter-uranus-equals-sun.md:13:activated_by: Sun
wiki/activations/jupiter-uranus-equals-sun.md:14:triad_set:
wiki/activations/jupiter-uranus-equals-sun.md:96:## Derived Synthesis
wiki/activations/sun-jupiter-equals-moon.md:3:page_type: activation
wiki/activations/sun-jupiter-equals-moon.md:11:normalized_formula: Sun/Jupiter = Moon
wiki/activations/sun-jupiter-equals-moon.md:12:axis: Sun/Jupiter
wiki/activations/sun-jupiter-equals-moon.md:13:activated_by: Moon
wiki/activations/sun-jupiter-equals-moon.md:14:triad_set:
wiki/activations/sun-jupiter-equals-moon.md:96:## Derived Synthesis
wiki/axes/jupiter-uranus.md:3:page_type: axis
wiki/axes/jupiter-uranus.md:10:normalized_axis: Jupiter/Uranus
wiki/axes/jupiter-uranus.md:30:  - Jupiter/Uranus = Sun
wiki/axes/jupiter-uranus.md:269:## Derived Synthesis
wiki/factors/sun.md:3:page_type: factor
wiki/factors/sun.md:238:## Derived Synthesis
wiki/axes/sun-moon.md:3:page_type: axis
wiki/axes/sun-moon.md:10:normalized_axis: Sun/Moon
wiki/axes/sun-moon.md:334:## Derived Synthesis
```

Observed page rules:

- `wiki/factors/sun.md`: `page_type: factor`, required `derived-synthesis` anchor present before `## Derived Synthesis`.
- `wiki/axes/sun-moon.md`: `page_type: axis`, `normalized_axis: Sun/Moon`, alias preserves unordered `Moon/Sun`, required anchor present.
- `wiki/axes/jupiter-uranus.md`: `page_type: axis`, `normalized_axis: Jupiter/Uranus`, related activation includes `Jupiter/Uranus = Sun`, required anchor present.
- `wiki/activations/jupiter-uranus-equals-sun.md`: `page_type: activation`, `normalized_formula: Jupiter/Uranus = Sun`, `axis: Jupiter/Uranus`, `activated_by: Sun`, required anchor present.
- `wiki/activations/sun-jupiter-equals-moon.md`: `page_type: activation`, `normalized_formula: Sun/Jupiter = Moon`, `axis: Sun/Jupiter`, `activated_by: Moon`, required anchor present.
- `wiki/triads/sun-jupiter-uranus.md`: `page_type: triad_hub`, unordered `triad_set` preserved, orientations list keeps `Jupiter/Uranus = Sun`, `Sun/Jupiter = Uranus`, and `Sun/Uranus = Jupiter` distinct.

