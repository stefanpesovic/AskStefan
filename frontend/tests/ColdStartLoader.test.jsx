import { render, screen, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import ColdStartLoader from "../src/components/ColdStartLoader";

describe("ColdStartLoader", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("renders initial status text", () => {
    render(<ColdStartLoader />);
    expect(screen.getByText("Waking up the server...")).toBeInTheDocument();
  });

  it("has pulsing animation class", () => {
    const { container } = render(<ColdStartLoader />);
    expect(container.querySelector(".animate-pulse")).toBeInTheDocument();
  });

  it("has spinning loader icon", () => {
    const { container } = render(<ColdStartLoader />);
    expect(container.querySelector(".animate-spin")).toBeInTheDocument();
  });

  it("cycles through status texts", () => {
    render(<ColdStartLoader />);
    expect(screen.getByText("Waking up the server...")).toBeInTheDocument();

    act(() => vi.advanceTimersByTime(3500));
    expect(screen.getByText("Loading the AI model...")).toBeInTheDocument();

    act(() => vi.advanceTimersByTime(3500));
    expect(screen.getByText("Almost ready...")).toBeInTheDocument();

    act(() => vi.advanceTimersByTime(3500));
    expect(screen.getByText("Any moment now...")).toBeInTheDocument();

    act(() => vi.advanceTimersByTime(3500));
    expect(screen.getByText("Waking up the server...")).toBeInTheDocument();
  });
});
