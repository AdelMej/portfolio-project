
import { apiFetch } from './client';

export async function getStripeOnboardingLink(): Promise<{ url: string }> {
  const res = await apiFetch('/coach/stripe/account', { method: 'POST' });
  return { url: res.onboarding_url };
}