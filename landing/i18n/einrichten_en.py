# -*- coding: utf-8 -*-
"""Texts for the setup pages (/en/einrichten/<slug>/). Structure lives in
`landing/einrichtungen.py`; every figure comes from `views.ANGEBOT_GROUPS`."""

EINRICHTEN = {
    # ════════════════════════════════════════════════════════════════════════
    "arbeitsplatz": {
        "titel": "Workstation setup for businesses — €190 fixed | WVM-IT",
        "desc": "A new workstation for €190: Windows, software, user account, email, "
                "printer, data transfer. Mostly remote, no contract. Get in touch.",
        "h1": "Have a workstation set up — fixed price, no contract",
        "nav": "Workstation setup",
        "kurz": "WVM-IT sets up a new workstation for €190: Windows, drivers, the "
                "programs the business actually uses, the user account, the mailbox, "
                "the printer, access to shared files and the transfer of everything "
                "from the old machine. It usually takes two to three hours and runs "
                "remotely, without anyone having to travel. No contract is needed; the "
                "price is per workstation.",
        "intro": "A new computer arrives, and from then on it gets tedious: Windows "
                 "wants setting up, the industry software needs its licence, the "
                 "mailbox should keep the old messages, the printer cannot be found, "
                 "and the files are still on the old machine. In practice that costs "
                 "half a working day to a full one — and it is the working day of "
                 "someone who has other things to do. That is what this fixed price is "
                 "for.",

        "leistungen_h": "What €190 includes",
        "leistungen": [
            "Setting up Windows, or configuring the pre-installed system, drivers "
            "included",
            "The programs the business needs: Office, industry software, PDF, browser, "
            "remote support access",
            "A user account with sensible permissions, a password rule and two-factor "
            "sign-in wherever it is available",
            "The mailbox with signature, folders and the old messages",
            "Access to shared files — on a server in the building or in the cloud",
            "Printer and multifunction device with the right drivers, including "
            "scanning into the correct folder",
            "Data transfer from the old machine: files, browser bookmarks, saved "
            "credentials",
            "Handover with a short briefing, so nothing is missing on day one",
        ],
        "nicht_h": "What it does not include",
        "nicht_t": "The hardware itself and the licences. We do not sell devices at a "
                   "markup: you buy wherever it is cheapest, or we order at cost. The "
                   "reason is simple — a dealer who earns on the hardware rarely "
                   "recommends the smaller machine. For office work, accounting and "
                   "industry software a mid-range computer with enough memory and an "
                   "SSD is almost always enough.",

        "ablauf_h": "How it works",
        "ablauf": [
            {"h": "A short call", "t": "Ten minutes on the phone: which programs, "
             "which mailbox, which printer, what should come across from the old machine."},
            {"h": "Setup, usually remote", "t": "You switch the computer on and start "
             "the remote session. We do the rest — two to three hours, with nobody "
             "having to sit next to it."},
            {"h": "Handover", "t": "A short briefing on where things are. After that "
             "our documentation records how this workstation is set up — also for the "
             "case that someone else has to take over later."},
        ],

        "fern_h": "Remote or on site?",
        "fern_t": "Most of it works remotely, and then the fixed price of €190 applies. "
                  "On site becomes necessary when the device has to be unpacked and "
                  "connected first, when several workstations are changed at once, or "
                  "when there is no working internet connection for the remote session. "
                  "An on-site visit costs €120 per hour plus travel; we say beforehand "
                  "whether it is needed and why.",

        "faq_h": "Common questions",
        "faq": [
            {"q": "Is the price per device or for all of them together?",
             "a": "Per workstation. Five new computers therefore cost five times €190. "
                  "With several devices at once it goes faster, because the setup only "
                  "has to be thought through once — we take that into account beforehand."},
            {"q": "What happens to the old computer?",
             "a": "On request we wipe it securely, so no company data is left on it. "
                  "What happens to the device afterwards — sold, passed on, disposed of "
                  "— is your decision."},
            {"q": "We have no IT support at all. Does this still work?",
             "a": "Yes, that is exactly what this fixed price is for. No contract and "
                  "no running support are needed. If you want one later, it starts at "
                  "€29 per workstation and month."},
            {"q": "And if a device is broken rather than new?",
             "a": "Then we first establish what is wrong. If it is the hard disk or the "
                  "memory, replacing it is usually still worth it. If it is the "
                  "mainboard or the power supply of an older machine, we advise "
                  "replacement — we do not carry out workshop repairs, because for "
                  "office equipment they are almost never cheaper than a new device."},
        ],

        "cta_h": "Request a workstation setup",
        "cta_t": "Tell us briefly how many devices are involved and what should run on "
                 "them. Reply within 24 hours.",
        "problem_h": "What is it about?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "pc-tausch": {
        "titel": "Replacing an old PC: data transfer for €190 | WVM-IT",
        "desc": "New computer, everything comes across: files, email, credentials, "
                "programs. €190 fixed per device, mostly remote. Get in touch.",
        "h1": "Replace a computer without losing anything",
        "nav": "Replacing a PC",
        "kurz": "When a device is replaced, WVM-IT moves everything that is needed — "
                "files, email including the folder structure, browser bookmarks, saved "
                "credentials and the configured programs — for €190 per workstation. "
                "The old machine is securely wiped on request. It usually runs remotely "
                "and takes two to three hours; the person working on it can carry on in "
                "the meantime.",
        "intro": "Replacing a device is the moment when data goes missing — not through "
                 "a fault, but through inconspicuousness. Files on the desktop are "
                 "noticed immediately. What is missing months later are the mails from "
                 "the local archive, the templates in a hidden Office folder, the "
                 "supplier logins saved in the browser, and the one spreadsheet someone "
                 "never put on the server. So nothing is copied because it catches the "
                 "eye; a list is worked through.",

        "leistungen_h": "What comes across",
        "leistungen": [
            "All files, including those outside the usual folders — desktop, downloads, "
            "local Office templates",
            "Email with folder structure, signatures, rules and local archives "
            "(old PST files included)",
            "Browser: bookmarks, saved credentials, start pages",
            "The business's programs, set up afresh rather than copied — with their "
            "settings where that is possible",
            "Printers, network drives and access to shared files",
            "A reconciliation at the end: what was on the old machine is on the new one",
            "Secure wiping of the old device on request",
        ],
        "nicht_h": "What it does not include",
        "nicht_t": "The new device and the licences. If programs are so old that they "
                   "no longer run on a current Windows, we say so beforehand — together "
                   "with what replacing them would cost. Recovering data from an "
                   "already failed hard disk is something different from a transfer and "
                   "is billed by effort.",

        "ablauf_h": "How it works",
        "ablauf": [
            {"h": "Taking stock on the old machine", "t": "We look at what is actually "
             "on it — not just what someone assumes. That becomes the list which is "
             "then worked through."},
            {"h": "The transfer", "t": "Two to three hours remotely. Both devices stay "
             "switched on; work can continue."},
            {"h": "Reconciliation and sign-off", "t": "We go through the list with you. "
             "Only once everything is there does the old device get wiped — not before."},
        ],

        "fern_h": "Why the old device does not go straight away",
        "fern_t": "There is a deliberate gap between transfer and wiping. What was "
                  "overlooked during the move rarely shows up on the same day, but in "
                  "the week after — the first time someone looks for an old template. "
                  "We therefore recommend leaving the old computer untouched for another "
                  "two to four weeks before it is wiped. Only then is the transfer "
                  "really finished.",

        "faq_h": "Common questions",
        "faq": [
            {"q": "Can we keep working while it happens?",
             "a": "Yes. The transfer runs in the background; we only need the device "
                  "briefly for the handover at the end. We agree a time that falls into "
                  "a quiet hour."},
            {"q": "What about our old industry software?",
             "a": "It is set up afresh, not copied — copied programs rarely run cleanly "
                  "on a new system. If licence keys or access details are needed for "
                  "that, we say beforehand which ones."},
            {"q": "The old computer will not start any more. Can it still be done?",
             "a": "Usually yes. As long as the hard disk is sound, we can reach the data "
                  "even on a dead machine. If the disk itself has failed, that is data "
                  "recovery — then we talk about effort and prospects beforehand, rather "
                  "than quoting a figure that cannot be held."},
            {"q": "Is replacing it worth it at all, or would an upgrade do?",
             "a": "That depends on age and condition. If the hard disk is still a "
                  "classic one and the computer is otherwise healthy, moving to an SSD "
                  "does more at every start-up than a new device would. Beyond roughly "
                  "six years it rarely pays off, because by then the power supply and "
                  "the fans are at the end too. We tell you what we would do in your "
                  "position."},
        ],

        "cta_h": "Request a device change",
        "cta_t": "Tell us briefly how many devices are being replaced and how old the "
                 "current ones are. Reply within 24 hours.",
        "problem_h": "What is it about?",
    },
}

HUB = {
    "titel": "Have IT set up: fixed prices from €190 | WVM-IT",
    "desc": "Workstation, PC replacement, Microsoft 365, server, network: single tasks "
            "at a fixed price, no contract. From €190, mostly remote. Get in touch.",
    "h1": "Single tasks — fixed price, no contract",
    "kurz": "WVM-IT handles single IT tasks at a fixed price, without any running "
            "support being necessary: setting up a workstation for €190, replacing a "
            "computer including the data transfer for €190. Most of it runs remotely "
            "across Austria and Germany; an on-site visit costs €120 per hour plus "
            "travel.",
    "intro": "Not every business needs running IT support. Sometimes there is simply a "
             "new computer on the desk, someone starts on Monday, or a device has "
             "reached the end. For those cases there are clear prices here and no "
             "contract — you commission a task, we do it, done. If more comes of it "
             "later, good; necessary it is not.",
    "abgrenzung_h": "And if it should be ongoing after all?",
    "abgrenzung_t": "Then the services pages are the right place. They are about support "
                    "that continues: keeping an eye on workstations and servers, "
                    "checking backups, being reachable when something stops. That starts "
                    "at €29 per workstation and month and is something other than a "
                    "single task — which is why it has its own pages.",
}
