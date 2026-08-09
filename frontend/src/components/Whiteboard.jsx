import React from 'react';
import { Stage, Layer, Rect, Circle, Line, Arrow, Text } from 'react-konva';
import * as math from 'mathjs';
import { useWhiteboardStore } from '../store/whiteboardStore';

const BOARD_WIDTH = 1000;
const BOARD_HEIGHT = 600;

function renderElement(el) {
  const { id, action, payload } = el;

  switch (action) {
    case 'draw_rectangle':
      return (
        <React.Fragment key={id}>
          <Rect x={payload.x} y={payload.y} width={payload.width} height={payload.height}
                stroke={payload.color || '#333'} strokeWidth={2} />
          {payload.label && (
            <Text x={payload.x} y={payload.y - 18} text={payload.label}
                  fontSize={14} fill={payload.color || '#333'} />
          )}
        </React.Fragment>
      );

    case 'draw_circle':
      return (
        <React.Fragment key={id}>
          <Circle x={payload.x} y={payload.y} radius={payload.radius}
                  stroke={payload.color || '#333'} strokeWidth={2} />
          {payload.label && (
            <Text x={payload.x - payload.radius} y={payload.y - payload.radius - 18}
                  text={payload.label} fontSize={14} fill={payload.color || '#333'} />
          )}
        </React.Fragment>
      );

    case 'draw_line':
      return (
        <Line key={id} points={[payload.x1, payload.y1, payload.x2, payload.y2]}
              stroke={payload.color || '#333'} strokeWidth={2} />
      );

    case 'draw_arrow':
      return (
        <Arrow key={id} points={[payload.x1, payload.y1, payload.x2, payload.y2]}
               stroke={payload.color || '#333'} fill={payload.color || '#333'} strokeWidth={2} />
      );

    case 'write_text':
      return (
        <Text key={id} x={payload.x} y={payload.y} text={payload.text}
              fontSize={payload.font_size || 18} fill={payload.color || '#111'} />
      );

    case 'write_code': {
      const lineCount = payload.code.split('\n').length;
      return (
        <React.Fragment key={id}>
          <Rect x={payload.x} y={payload.y} width={380} height={20 * lineCount + 16}
                fill="#1e1e1e" cornerRadius={6} />
          <Text x={payload.x + 10} y={payload.y + 8} text={payload.code}
                fontFamily="monospace" fontSize={13} fill="#d4d4d4" />
        </React.Fragment>
      );
    }

    case 'plot_function': {
      const { expression, x_min = -10, x_max = 10, x, y, width, height, color } = payload;
      let rawPoints = [];
      try {
        const compiled = math.compile(expression);
        const steps = 100;
        for (let i = 0; i <= steps; i++) {
          const xi = x_min + (i / steps) * (x_max - x_min);
          const yi = compiled.evaluate({ x: xi });
          rawPoints.push([xi, yi]);
        }
      } catch (e) {
        console.error('plot_function failed to evaluate:', expression, e);
        return null;
      }

      const yValues = rawPoints.map((p) => p[1]).filter(Number.isFinite);
      const yMin = Math.min(...yValues);
      const yMax = Math.max(...yValues);
      const yRange = yMax - yMin || 1;

      const points = rawPoints.flatMap(([xi, yi]) => [
        x + ((xi - x_min) / (x_max - x_min)) * width,
        y + height - ((yi - yMin) / yRange) * height,
      ]);

      return (
        <React.Fragment key={id}>
          <Rect x={x} y={y} width={width} height={height} stroke="#ddd" strokeWidth={1} />
          <Line points={points} stroke={color || '#2563eb'} strokeWidth={2} />
        </React.Fragment>
      );
    }

    default:
      return null;
  }
}

export function Whiteboard() {
  const elements = useWhiteboardStore((state) => state.elements);
  return (
    <Stage width={BOARD_WIDTH} height={BOARD_HEIGHT}
           style={{ border: '1px solid #ccc', background: '#fff' }}>
      <Layer>{elements.map(renderElement)}</Layer>
    </Stage>
  );
}