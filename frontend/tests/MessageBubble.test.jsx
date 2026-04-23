import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import MessageBubble from "../src/components/MessageBubble";

describe("MessageBubble", () => {
  it("renders user message content", () => {
    render(<MessageBubble role="user" content="What are your skills?" />);
    expect(screen.getByText("What are your skills?")).toBeInTheDocument();
  });

  it("renders assistant message content", () => {
    render(
      <MessageBubble role="assistant" content="I have Python experience." />
    );
    expect(screen.getByText("I have Python experience.")).toBeInTheDocument();
  });

  it("applies violet styling for user messages", () => {
    const { container } = render(
      <MessageBubble role="user" content="Hello" />
    );
    const bubble = container.querySelector(".bg-violet-500\\/20");
    expect(bubble).toBeInTheDocument();
  });

  it("applies glass styling for assistant messages", () => {
    const { container } = render(
      <MessageBubble role="assistant" content="Hi there" />
    );
    const bubble = container.querySelector(".glass");
    expect(bubble).toBeInTheDocument();
  });

  it("aligns user messages to the right", () => {
    const { container } = render(
      <MessageBubble role="user" content="Test" />
    );
    const justifyEl = container.querySelector(".justify-end");
    expect(justifyEl).toBeInTheDocument();
  });

  it("aligns assistant messages to the left", () => {
    const { container } = render(
      <MessageBubble role="assistant" content="Test" />
    );
    const justifyEl = container.querySelector(".justify-start");
    expect(justifyEl).toBeInTheDocument();
  });
});
