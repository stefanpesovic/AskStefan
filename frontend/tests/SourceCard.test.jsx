import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import SourceCard from "../src/components/SourceCard";

const mockSource = {
  chunk_id: "cv_pdf__page_1__0",
  source_file: "cv.pdf",
  source_type: "resume",
  location: "page 1",
  text: "Experienced Python developer with FastAPI and React skills.",
  similarity_score: 0.87,
};

describe("SourceCard", () => {
  it("renders source filename", () => {
    render(<SourceCard source={mockSource} query="" index={0} />);
    expect(screen.getByText("cv.pdf")).toBeInTheDocument();
  });

  it("renders source type badge", () => {
    render(<SourceCard source={mockSource} query="" index={0} />);
    expect(screen.getByText("Resume")).toBeInTheDocument();
  });

  it("renders location", () => {
    render(<SourceCard source={mockSource} query="" index={0} />);
    expect(screen.getByText("page 1")).toBeInTheDocument();
  });

  it("renders similarity percentage", () => {
    render(<SourceCard source={mockSource} query="" index={0} />);
    expect(screen.getByText("87%")).toBeInTheDocument();
  });

  it("highlights matching words from query", () => {
    const { container } = render(
      <SourceCard source={mockSource} query="Python skills" index={0} />
    );
    const marks = container.querySelectorAll("mark");
    expect(marks.length).toBeGreaterThan(0);
    const highlighted = Array.from(marks).map((m) => m.textContent.toLowerCase());
    expect(highlighted).toContain("python");
  });

  it("does not highlight stopwords", () => {
    const { container } = render(
      <SourceCard source={mockSource} query="with and the" index={0} />
    );
    const marks = container.querySelectorAll("mark");
    expect(marks.length).toBe(0);
  });

  it("renders project type badge for project sources", () => {
    const projectSource = {
      ...mockSource,
      source_type: "project_description",
      source_file: "projects.md",
    };
    render(<SourceCard source={projectSource} query="" index={0} />);
    expect(screen.getByText("Project")).toBeInTheDocument();
  });
});
