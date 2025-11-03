import { act } from '@testing-library/react';
import { useAuth } from '../lib/store';

describe('useAuth store', () => {
  beforeEach(() => {
    act(() => {
      useAuth.setState({ user: null, initialized: false });
    });
  });

  it('stores and clears the current user', () => {
    const sampleUser = { id: 1, username: 'demo', email: 'demo@example.com' };
    act(() => {
      useAuth.getState().setUser(sampleUser);
    });
    expect(useAuth.getState().user).toEqual(sampleUser);

    act(() => {
      useAuth.getState().clear();
    });
    expect(useAuth.getState().user).toBeNull();
    expect(useAuth.getState().initialized).toBe(true);
  });
});
