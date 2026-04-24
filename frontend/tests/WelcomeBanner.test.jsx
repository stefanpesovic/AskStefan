import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, beforeEach } from "vitest";
import WelcomeBanner from "../src/components/WelcomeBanner";

describe("WelcomeBanner", () => {
  beforeEach(() => {
    sessionStorage.clear();
  });

  it("renders welcome message", () => {
    render(<WelcomeBanner />);
    expect(screen.getByText(/This chatbot is a portfolio piece/)).toBeInTheDocument();
  });

  it("renders dismiss button", () => {
    render(<WelcomeBanner />);
    expect(screen.getByRole("button", { name: /dismiss/i })).toBeInTheDocument();
  });

  it("hides banner when X is clicked", async () => {
    render(<WelcomeBanner />);
    fireEvent.click(screen.getByRole("button", { name: /dismiss/i }));
    await waitFor(() => {
      expect(screen.queryByText(/This chatbot is a portfolio piece/)).not.toBeInTheDocument();
    });
  });

  it("sets sessionStorage on dismiss", () => {
    render(<WelcomeBanner />);
    fireEvent.click(screen.getByRole("button", { name: /dismiss/i }));
    expect(sessionStorage.getItem("welcomeBannerDismissed")).toBe("true");
  });

  it("does not render if sessionStorage flag is set", () => {
    sessionStorage.setItem("welcomeBannerDismissed", "true");
    render(<WelcomeBanner />);
    expect(screen.queryByText(/This chatbot is a portfolio piece/)).not.toBeInTheDocument();
  });
});
