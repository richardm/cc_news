"""Generate Markdown documentation from a Click CLI command tree."""

import click


def generate_docs(group: click.Command, prog_name: str = "cc-news") -> str:
    """Walk a Click command tree and return Markdown documentation.

    Args:
        group: The root Click group or command.
        prog_name: The name to display for the CLI program.

    Returns:
        A Markdown-formatted string documenting every command.
    """
    lines: list[str] = []

    # Root heading and description
    ctx = click.Context(group, info_name=prog_name)
    lines.append(f"# {prog_name}")
    lines.append("")
    if group.help:
        lines.append(group.help.strip())
        lines.append("")

    # Command table (if the root is a group with subcommands)
    commands = _get_commands(group)
    if commands:
        lines.append("| Command | Description |")
        lines.append("|---------|-------------|")
        for name, cmd in commands:
            short_help = cmd.get_short_help_str(limit=80)
            lines.append(f"| `{prog_name} {name}` | {short_help} |")
        lines.append("")

    # Per-command sections
    for name, cmd in commands:
        lines.extend(_format_command(cmd, name, prog_name, ctx))

    return "\n".join(lines)


def _get_commands(
    group: click.Command,
) -> list[tuple[str, click.Command]]:
    """Return a sorted list of (name, command) pairs for a group."""
    if not isinstance(group, click.Group):
        return []
    names = group.list_commands(click.Context(group))
    result = []
    for name in sorted(names):
        cmd = group.get_command(click.Context(group), name)
        if cmd is not None:
            result.append((name, cmd))
    return result


def _format_command(
    cmd: click.Command,
    name: str,
    prog_name: str,
    parent_ctx: click.Context,
) -> list[str]:
    """Format a single command as Markdown lines."""
    lines: list[str] = []
    ctx = click.Context(cmd, info_name=name, parent=parent_ctx)
    full_name = f"{prog_name} {name}"

    # Section heading
    lines.append(f"## {full_name}")
    lines.append("")

    # Description
    if cmd.help:
        lines.append(cmd.help.strip())
        lines.append("")

    # Usage block
    formatter = ctx.make_formatter()
    pieces = cmd.collect_usage_pieces(ctx)
    formatter.write_usage(full_name, " ".join(pieces))
    usage_text = formatter.getvalue().strip()
    lines.append("```")
    lines.append(usage_text)
    lines.append("```")
    lines.append("")

    # Parameters table
    params = [p for p in cmd.params if p.name != "help"]
    if params:
        lines.append("| Parameter | Type | Required | Default | Description |")
        lines.append("|-----------|------|----------|---------|-------------|")
        for param in params:
            lines.extend(_format_param(param))
        lines.append("")

    return lines


def _format_param(param: click.Parameter) -> list[str]:
    """Format a single Click parameter as a Markdown table row."""
    if isinstance(param, click.Argument):
        display_name = f"`{param.human_readable_name}`"
        param_type = "argument"
    else:
        # Option -- show the long/short flags
        opts = " / ".join(param.opts)
        if param.secondary_opts:
            opts += " / " + " / ".join(param.secondary_opts)
        display_name = f"`{opts}`"
        param_type = "option"

    required = "yes" if param.required else "no"
    raw_default = param.default
    is_sentinel = "UNSET" in str(raw_default)
    default = "—" if raw_default is None or is_sentinel else raw_default
    description = getattr(param, "help", None) or ""

    row = f"| {display_name} | {param_type} | {required} | {default} | {description} |"
    return [row]


def main() -> None:
    """Entry point for running as ``python -m cc_news_analyzer.generate_docs``."""
    from cc_news_analyzer.cli import cli

    print(generate_docs(cli))


if __name__ == "__main__":
    main()
