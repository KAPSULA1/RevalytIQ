import { fetchKPIs, fetchOrders } from '../lib/auth';
import { api } from '../lib/api';

describe('analytics api helpers', () => {
  it('fetchKPIs returns the data payload', async () => {
    const payload = { revenue: 1000, orders: 4, aov: 250 };
    const spy = jest.spyOn(api, 'get').mockResolvedValueOnce({ data: payload } as any);
    await expect(fetchKPIs()).resolves.toEqual(payload);
    expect(spy).toHaveBeenCalledWith('/api/analytics/kpis/');
    spy.mockRestore();
  });

  it('fetchOrders returns list or paginated payload', async () => {
    const payload = { count: 1, results: [{ id: 1 }] };
    const spy = jest.spyOn(api, 'get').mockResolvedValueOnce({ data: payload } as any);
    await expect(fetchOrders()).resolves.toEqual(payload);
    expect(spy).toHaveBeenCalledWith('/api/analytics/orders/');
    spy.mockRestore();
  });
});
