from __future__ import annotations

import argparse
import json

from tools.wiki_identity import normalize_activation, normalize_axis, triad_orientations


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    axis_parser = subparsers.add_parser("axis")
    axis_parser.add_argument("factor_a")
    axis_parser.add_argument("factor_b")

    activation_parser = subparsers.add_parser("activation")
    activation_parser.add_argument("factor_a")
    activation_parser.add_argument("factor_b")
    activation_parser.add_argument("activated_by")

    triad_parser = subparsers.add_parser("triad")
    triad_parser.add_argument("factors", nargs=3)

    args = parser.parse_args()

    if args.command == "axis":
        identity = normalize_axis(args.factor_a, args.factor_b)
        payload = {"display": identity.display, "slug": identity.slug, "factors": identity.factors}
    elif args.command == "activation":
        identity = normalize_activation(args.factor_a, args.factor_b, args.activated_by)
        payload = {
            "display": identity.display,
            "slug": identity.slug,
            "axis": identity.axis.display,
            "activated_by": identity.activated_by,
            "triad_set": identity.triad_set,
        }
    else:
        payload = {"orientations": triad_orientations(args.factors)}

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
