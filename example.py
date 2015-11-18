#!/usr/bin/env python

import svg


def main():
    root = svg.Svg()
    root.add_definition("sq", svg.Rect(x=0, y=0, height=10, width=20))

    complex = svg.Group()
    complex.children.append(svg.Rect(x=0, y=0, height=10, width=10))
    complex.children.append(svg.Rect(x=10, y=10, height=10, width=20))

    root.add_definition("complex", complex)

    root.children.append(svg.Use("sq", x=10))
    root.children.append(svg.Use("complex"))




    print(root)


if __name__ == "__main__":
    main()
