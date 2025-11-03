import { render } from '@testing-library/react';
import Dashboard from '../app/dashboard/page';
import { useAuth } from '../lib/store';

const replaceMock = jest.fn();

jest.mock('next/navigation', () => ({
  useRouter: () => ({ replace: replaceMock }),
}));

jest.mock('@tanstack/react-query', () => ({
  useQuery: () => ({ data: undefined, isLoading: false, isError: false }),
  useQueryClient: () => ({ invalidateQueries: jest.fn() }),
}));

jest.mock('react-hot-toast', () => ({ success: jest.fn() }));

jest.mock('../components/Navbar', () => () => <div data-testid="navbar" />);
jest.mock('../components/Sidebar', () => () => <div data-testid="sidebar" />);
jest.mock('../app/dashboard/components/KPIStat', () => () => <div data-testid="kpi" />);
jest.mock('../app/dashboard/components/RevenueChart', () => () => <div data-testid="chart" />);
jest.mock('../app/dashboard/components/OrdersTable', () => () => <div data-testid="orders-table" />);

const resetAuthStore = () => {
  useAuth.setState({ user: null, initialized: false });
  replaceMock.mockClear();
};

describe('Dashboard auth guard', () => {
  beforeEach(() => {
    resetAuthStore();
  });

  it('redirects to login when unauthenticated', () => {
    useAuth.setState({ user: null, initialized: true });
    render(<Dashboard />);
    expect(replaceMock).toHaveBeenCalledWith('/');
  });

  it('renders dashboard when user is present', () => {
    useAuth.setState({
      user: { id: 1, username: 'demo', email: 'demo@example.com' },
      initialized: true,
    });
    const { getByTestId } = render(<Dashboard />);
    expect(replaceMock).not.toHaveBeenCalled();
    expect(getByTestId('navbar')).toBeInTheDocument();
  });
});
