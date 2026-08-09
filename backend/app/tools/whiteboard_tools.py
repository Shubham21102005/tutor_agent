WHITEBOARD_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "draw_rectangle",
            "description": "Draw a rectangle outline on the whiteboard. Use for boxes, diagram nodes, or framing content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "Top-left x coordinate (0-1000)"},
                    "y": {"type": "number", "description": "Top-left y coordinate (0-600)"},
                    "width": {"type": "number"},
                    "height": {"type": "number"},
                    "color": {"type": "string", "description": "Hex color, e.g. #2563eb. Optional."},
                    "label": {"type": "string", "description": "Optional short text label above the rectangle."},
                },
                "required": ["x", "y", "width", "height"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "draw_circle",
            "description": "Draw a circle outline on the whiteboard. Use for nodes, cells, atoms, or round diagram elements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "number", "description": "Center x coordinate (0-1000)"},
                    "y": {"type": "number", "description": "Center y coordinate (0-600)"},
                    "radius": {"type": "number"},
                    "color": {"type": "string"},
                    "label": {"type": "string"},
                },
                "required": ["x", "y", "radius"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "draw_line",
            "description": "Draw a straight line between two points. Use for connectors, underlines, or axes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x1": {"type": "number"}, "y1": {"type": "number"},
                    "x2": {"type": "number"}, "y2": {"type": "number"},
                    "color": {"type": "string"},
                },
                "required": ["x1", "y1", "x2", "y2"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "draw_arrow",
            "description": "Draw an arrow from one point to another. Use to show direction, flow, or relationships between elements.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x1": {"type": "number"}, "y1": {"type": "number"},
                    "x2": {"type": "number"}, "y2": {"type": "number"},
                    "color": {"type": "string"},
                },
                "required": ["x1", "y1", "x2", "y2"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_text",
            "description": "Write a short text label or annotation at a position on the whiteboard.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "number"}, "y": {"type": "number"},
                    "text": {"type": "string"},
                    "font_size": {"type": "number", "description": "Optional, default 18"},
                    "color": {"type": "string"},
                },
                "required": ["x", "y", "text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_code",
            "description": "Write a block of code on the whiteboard, monospaced. Use when explaining or writing out code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "x": {"type": "number"}, "y": {"type": "number"},
                    "code": {"type": "string", "description": "The code content, with real newlines."},
                    "language": {"type": "string", "description": "Optional, e.g. 'python', 'javascript'."},
                },
                "required": ["x", "y", "code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "plot_function",
            "description": "Plot a mathematical function of x on a graph. Use for equations, curves, and visualizing math concepts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "A math expression in terms of x, e.g. 'x^2 + 2*x - 3'."},
                    "x_min": {"type": "number", "description": "Optional, default -10"},
                    "x_max": {"type": "number", "description": "Optional, default 10"},
                    "x": {"type": "number", "description": "Top-left x of the plot area on the board"},
                    "y": {"type": "number", "description": "Top-left y of the plot area on the board"},
                    "width": {"type": "number", "description": "Plot area width, e.g. 300"},
                    "height": {"type": "number", "description": "Plot area height, e.g. 200"},
                    "color": {"type": "string"},
                },
                "required": ["expression", "x", "y", "width", "height"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "clear_board",
            "description": "Clear everything currently drawn on the whiteboard. Use when starting a new, unrelated topic or diagram.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
    "type": "function",
    "function": {
        "name": "draw_polygon",
        "description": "Draw a closed shape (e.g. a triangle) by connecting a list of points in order, then closing back to the first point. Use this instead of chaining multiple draw_line calls for triangles or other multi-sided shapes.",
        "parameters": {
            "type": "object",
            "properties": {
                "points": {
                    "type": "array",
                    "description": "List of vertices in order, e.g. three points for a triangle.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number"},
                            "y": {"type": "number"},
                        },
                        "required": ["x", "y"],
                    },
                },
                "color": {"type": "string"},
                "label": {"type": "string"},
            },
            "required": ["points"],
        },
    },
},
]