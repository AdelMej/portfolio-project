
import { apiFetch } from './client';

export async function getStripeOnboardingLink(): Promise<{ url: string }> {
  return apiFetch('/stripe/onboarding-link');
}