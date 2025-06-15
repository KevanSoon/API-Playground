// store/useRouteStore.ts
import { create } from 'zustand'

type RouteState = {
  selectedRoute: string
  setSelectedRoute: (route: string) => void
}

export const useRouteStore = create<RouteState>((set) => ({
  selectedRoute: 'Dashboard',
  setSelectedRoute: (route) => set({ selectedRoute: route }),
}))
