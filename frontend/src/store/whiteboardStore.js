import { create } from 'zustand';

let idCounter = 0;

export const useWhiteboardStore = create((set) => ({
  elements: [],
  addElement: (action, payload) =>
    set((state) => ({
      elements: [...state.elements, { id: `el-${idCounter++}`, action, payload }],
    })),
  clearBoard: () => set({ elements: [] }),
}));