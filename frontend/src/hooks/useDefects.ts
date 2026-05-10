import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { defectsApi } from '../api/defects';
import type { Defect, DefectCreate, DefectUpdate, DefectStatus } from '@/types/defect';

export function useDefects() {
  return useQuery<Defect[], Error>({
    queryKey: ['defects'],
    queryFn: () => defectsApi.list(), 
  });
}

export function useDefect(id: string) {
  return useQuery<Defect, Error>({
    queryKey: ['defects', id],
    queryFn: () => defectsApi.get(id),
  });
}

export function useCreateDefect() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: DefectCreate) => defectsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['defects'] });
    },
  });
}

export function useUpdateDefect() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<DefectUpdate> }) => 
      defectsApi.update(id, data),
    onMutate: async ({ id, data }) => {
      await queryClient.cancelQueries({ queryKey: ['defects'] });
      const previousDefects = queryClient.getQueryData<Defect[]>(['defects']);

      if (previousDefects) {
        queryClient.setQueryData<Defect[]>(['defects'], 
          previousDefects.map(d => d.id === id ? { ...d, ...data } : d)
        );
      }

      return { previousDefects };
    },
    onError: (_err, _variables, context) => {
      if (context?.previousDefects) {
        queryClient.setQueryData(['defects'], context.previousDefects);
      }
      // Suggestion: Trigger a toast notification here
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['defects'] });
    },
  });
}

export function useTransitionDefectStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, newStatus }: { id: string; newStatus: DefectStatus }) => 
      defectsApi.transitionStatus(id, newStatus),
    // Optimistic Update Implementation
    onMutate: async ({ id, newStatus }) => {
      // Cancel any outgoing refetches so they don't overwrite our optimistic update
      await queryClient.cancelQueries({ queryKey: ['defects'] });

      // Snapshot the previous value
      const previousDefects = queryClient.getQueryData<Defect[]>(['defects']);

      // Optimistically update to the new value
      if (previousDefects) {
        queryClient.setQueryData<Defect[]>(['defects'], 
          previousDefects.map(d => d.id === id ? { ...d, status: newStatus } : d)
        );
      }

      return { previousDefects };
    },
    onError: (_err, _variables, context) => {
      // Roll back to the previous state if the mutation fails
      if (context?.previousDefects) {
        queryClient.setQueryData(['defects'], context.previousDefects);
      }
    },
    onSettled: () => {
      // Always refetch after error or success to ensure sync with server
      queryClient.invalidateQueries({ queryKey: ['defects'] });
    },
  });
}
