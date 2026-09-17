# Security Policy

## Supported version

Security and reliability fixes are applied to the current 2.x line.

## Scope

MacTrix is a local synthetic-data generator and validator. It does not modify network adapters, perform network discovery, send generated data to remote services or contain MAC-spoofing/bypass functionality.

## Reporting

Please report a suspected vulnerability privately through GitHub's security reporting features when available. Avoid posting sensitive reproduction details in a public issue before a fix is available.

A useful report should include the affected version, operating system, reproduction steps, expected behavior and actual behavior.

## Generated data

Generated addresses use locally administered unicast semantics and synthetic profile prefixes. They are intended for tests, labs and development and should not be treated as real vendor identities.
