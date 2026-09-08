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

    # ════════════════════════════════════════════════════════════════════════
    "windows-11": {
        "titel": "Windows 11 migration — €190 per device | WVM-IT",
        "desc": "Windows 10 has had no security updates since October 2025. Migration "
                "per workstation €190, including a check of your programs. Get in touch.",
        "h1": "Windows 11 in the business: migrate or replace the device?",
        "nav": "Windows 11",
        "kurz": "Windows 10 has received no security updates since October 2025. For "
                "each workstation WVM-IT checks whether the device supports Windows 11 "
                "at all and whether the programs in use will run on it, then carries "
                "out the migration — €190 per workstation. Where the hardware cannot "
                "follow, we say so beforehand rather than discovering it mid-migration.",
        "intro": "The move is easily postponed because nothing hurts: Windows 10 still "
                 "starts, the programs run, it looks like it always did. Missing "
                 "security updates are not noticed — until the day they would have "
                 "mattered. The same calm creates the second trap: whoever migrates only "
                 "when it is urgent discovers on the same day that two machines do not "
                 "meet the requirements and the industry software needs a new version.",

        "leistungen_h": "What €190 per workstation includes",
        "leistungen": [
            "A check of whether the device supports Windows 11 — processor, memory, "
            "TPM 2.0, Secure Boot",
            "A check of whether the programs in use will run on it, especially industry "
            "and accounting software",
            "The migration itself, with a backup taken beforehand",
            "Settings, accounts, printers and network drives as before",
            "Follow-up: whatever looks different after the move gets put right",
            "A list of the devices that cannot follow — with what a replacement costs",
        ],
        "nicht_h": "What it does not include",
        "nicht_t": "New hardware and licences for programs that need a newer version. If "
                   "a device does not meet the requirements the check is still worth it "
                   "— it then costs nothing extra, and you know where you stand. If it "
                   "turns into a device replacement, the same price applies as for a "
                   "computer change, not both together.",

        "ablauf_h": "How it works",
        "ablauf": [
            {"h": "Taking stock", "t": "We look at every workstation and sort them into "
             "three groups: ready now, ready with effort, not possible."},
            {"h": "One device first", "t": "We migrate a single workstation first — the "
             "one running the most critical software. Only when nothing shows up there "
             "for a week does the rest follow."},
            {"h": "The rest, in groups", "t": "Not all on one day. That keeps the "
             "business working even if something has to be sorted out."},
        ],

        "fern_h": "What happens to devices that cannot follow?",
        "fern_t": "There are three routes, and we say openly which one applies when. If "
                  "the computer is otherwise healthy and only fails on TPM 2.0, on many "
                  "devices that can be enabled in the BIOS afterwards — then it costs "
                  "nothing further. If it is older than roughly six years, replacement "
                  "pays off. And for machine controllers that have to run an old Windows "
                  "version, there is a fourth route: they get separated from the rest of "
                  "the network instead of being migrated.",

        "faq_h": "Common questions",
        "faq": [
            {"q": "How urgent is this really?",
             "a": "Without security updates, every newly found gap stays open "
                  "permanently. This is not a state that turns dangerous overnight after "
                  "a deadline, but one that gets slightly worse every month. Anyone "
                  "still on Windows 10 should plan the move — not tonight, but this "
                  "quarter."},
            {"q": "Will our industry software run under Windows 11?",
             "a": "We check that before the migration, not after. For most programs it "
                  "is unproblematic; for older specialist applications we ask the "
                  "manufacturer and tell you what a current version costs before "
                  "anything is touched."},
            {"q": "Can we stay on Windows 10 and pay for it?",
             "a": "Microsoft offers businesses extended security updates for a fee that "
                  "rises year on year. That can make sense for individual special cases "
                  "— as a permanent solution for a whole business it almost never adds "
                  "up against migrating."},
            {"q": "What about computers that only control a machine?",
             "a": "We usually do not migrate those. Touching a controller that has run "
                  "for years is the greater risk. The right route is to separate it from "
                  "the rest of the network — there is a separate article on that."},
        ],

        "cta_h": "Request a migration",
        "cta_t": "Tell us briefly how many workstations are still on Windows 10. Reply "
                 "within 24 hours.",
        "problem_h": "What is it about?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "microsoft-365": {
        "titel": "Microsoft 365 setup — €290 fixed price | WVM-IT",
        "desc": "Mailboxes, Teams, OneDrive and SharePoint set up properly: €290 fixed, "
                "including migration of your existing email. Get in touch.",
        "h1": "Microsoft 365 setup — once properly instead of three times halfway",
        "nav": "Microsoft 365",
        "kurz": "WVM-IT sets up Microsoft 365 for €290: mailboxes and aliases, "
                "two-factor sign-in, Teams, OneDrive and the shared filing in "
                "SharePoint, plus the migration of your existing email including folders "
                "and calendars. The price covers the setup; you pay the licences "
                "directly to Microsoft.",
        "intro": "Microsoft 365 is bought in ten minutes and still not properly set up "
                 "ten months later. That is the normal case: the mailboxes run, "
                 "everything else gets placed alongside bit by bit. Files exist three "
                 "times over — in one person's OneDrive, attached to an email, and on "
                 "the old server. Whoever leaves takes their access with them. And "
                 "nobody knows where the current version of the quote is.",

        "leistungen_h": "What €290 includes",
        "leistungen": [
            "Mailboxes, aliases, distribution lists and shared mailboxes",
            "Two-factor sign-in for every account — the single most effective step "
            "against taken-over accounts",
            "Migration of existing email with folders, calendars and contacts",
            "Teams with a structure that fits the business rather than the promo video",
            "OneDrive and SharePoint kept apart: personal and shared, so it is clear "
            "what stays when someone leaves",
            "Permissions: who sees what, and what happens when someone goes",
            "Setup on the workstations and on the phones",
        ],
        "nicht_h": "What it does not include",
        "nicht_t": "The licences. You buy those directly from Microsoft or through a "
                   "reseller — we add nothing on top. We tell you beforehand which tier "
                   "you need: for most businesses the smaller one is enough, and the "
                   "difference costs more per person and year than this setup does once.",

        "ablauf_h": "How it works",
        "ablauf": [
            {"h": "What goes where", "t": "A conversation about the structure: which "
             "departments, which shared filing, who may see what. That is the part that "
             "saves trouble later."},
            {"h": "Setup and migration", "t": "The mailboxes are migrated while the old "
             "ones keep running. There is no day without email."},
            {"h": "Switch over and brief", "t": "The switch happens in an evening. The "
             "next morning we show what has changed."},
        ],

        "fern_h": "Why the structure matters more than the setup",
        "fern_t": "Setting up a mailbox takes minutes. The question that counts years "
                  "later is a different one: where do the files live that belong to "
                  "several people? Someone working in OneDrive for weeks has filed their "
                  "documents personally — and when that person leaves the business, the "
                  "documents go with their account. So we separate from the start: "
                  "personal in OneDrive, shared in SharePoint. That is less convenient "
                  "on day one and the whole difference at the first departure.",

        "faq_h": "Common questions",
        "faq": [
            {"q": "Will we lose old email in the migration?",
             "a": "No. The mailboxes are taken over with their folder structure, "
                  "calendars and contacts, and the old ones keep running throughout. "
                  "Only once everything is there do we switch over."},
            {"q": "Does the price hold regardless of the number of mailboxes?",
             "a": "For a typical business up to around fifteen mailboxes, yes. Above "
                  "that we say beforehand what is added — usually less than people "
                  "expect, because the structure is only built once."},
            {"q": "We already have Microsoft 365, but it is a mess.",
             "a": "That is the more common case. Then it is not about setup but about "
                  "tidying up: sorting permissions, merging filing, adding two-factor. "
                  "We bill that by effort, because the scope cannot be quoted in "
                  "advance — after a short look we name an upper limit."},
        ],

        "cta_h": "Ask about Microsoft 365",
        "cta_t": "Tell us briefly how many mailboxes there will be and whether anything "
                 "already exists. Reply within 24 hours.",
        "problem_h": "What is it about?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "server": {
        "titel": "Server setup for small businesses | WVM-IT",
        "desc": "Setting up a server: users, shares, permissions, backup — on site or "
                "virtual. Price after taking stock, support afterwards from €89/month. "
                "Get in touch.",
        "h1": "A server set up to still carry you in five years",
        "nav": "Server setup",
        "kurz": "WVM-IT sets up servers for small and medium businesses: operating "
                "system, users and permissions, shared folders, backup and remote "
                "access — in the building or virtual. What it costs we say after taking "
                "stock, because it depends on size, existing equipment and requirements. "
                "The monitoring afterwards starts at €89 a month.",
        "intro": "A server is not a purchase but a decision for the next five years. "
                 "Most mistakes happen not with the hardware but with the structure: "
                 "shares that grew historically, permissions nobody can explain any "
                 "more, and a backup that runs but has never been restored. So it starts "
                 "with a survey of what is there — and only then a price.",

        "leistungen_h": "What is involved",
        "leistungen": [
            "Advice on whether a server is needed at all — for some businesses the "
            "cloud is the cheaper route, and we say so",
            "Operating system, basic hardening and updates",
            "Users, groups and permissions in a structure that can still be explained "
            "later",
            "Shared folders, cleanly separated by department and purpose",
            "Backup kept separate from the server — and a test restore before we are "
            "finished",
            "Remote access over VPN where it is needed",
            "Documentation another provider could carry on with",
        ],
        "nicht_h": "Why there is no fixed price here",
        "nicht_t": "Because it could not be held. Whether a business needs a small file "
                   "server or a machine running the industry software for twenty people "
                   "makes a difference of days. We quote in writing after taking stock — "
                   "before the first move, and then it holds. The survey itself is "
                   "billed by the hour (€95 remote, €120 on site plus travel); if it "
                   "becomes an order, it is credited.",

        "ablauf_h": "How it works",
        "ablauf": [
            {"h": "Taking stock", "t": "What is there today, what has to run on it, how "
             "many people access it, what is the longest outage the business can take."},
            {"h": "A quote with numbers", "t": "In writing, with hardware, work and "
             "running costs listed separately. If the cloud would be cheaper, it says so."},
            {"h": "Build and handover", "t": "Setup happens outside working hours. The "
             "handover includes a tested restore — a backup that has never been restored "
             "is a hope."},
        ],

        "fern_h": "Server in the building or in the cloud?",
        "fern_t": "The question comes before the setup, and the answer is not always the "
                  "server. For businesses whose work depends on software that requires "
                  "one, or that move large amounts of data on site, it remains the right "
                  "choice. Anyone mainly sharing files and writing email is usually "
                  "better off in the cloud, both in cost and in effort. We work both "
                  "through over three years — including electricity, an uninterruptible "
                  "power supply and the time for updates, which a pure purchase "
                  "comparison leaves out.",

        "faq_h": "Common questions",
        "faq": [
            {"q": "How long does the setup take?",
             "a": "A file server for a small business is ready in a day. With industry "
                  "software, terminal services or a migration of existing data it becomes "
                  "two to four. We give the range in the quote."},
            {"q": "Do we have to take a support contract afterwards?",
             "a": "No. You get the documentation and the access details and can work with "
                  "them or commission someone else. If you want the monitoring it starts "
                  "at €89 a month — then we see disk space, load and failed backups "
                  "before you notice them."},
            {"q": "We already have a server, but nobody knows it any more.",
             "a": "That is a common case too. Then it starts with a survey of what runs "
                  "and an honest assessment: keep it, rebuild it, or replace it. Taking "
                  "over an undocumented system is work — but usually less than a new "
                  "build."},
        ],

        "cta_h": "Ask about a server setup",
        "cta_t": "Tell us briefly how many workstations will use it and what should run "
                 "on the server. Reply within 24 hours.",
        "problem_h": "What is it about?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "netzwerk": {
        "titel": "Office network setup — from €890 | WVM-IT",
        "desc": "Router, switch, Wi-Fi, printers on the network and a separate guest "
                "network — set up and surveyed from €890. Get in touch.",
        "h1": "A network that carries through the whole building",
        "nav": "Network setup",
        "kurz": "WVM-IT sets up business networks from €890: configuring router and "
                "switch, placing and surveying Wi-Fi so it carries everywhere, "
                "connecting printers and network drives, setting up a separate guest "
                "network. For cabling, halls and multiple floors we quote after a "
                "survey — the starting price covers an office of usual size.",
        "intro": "Network problems are rarely loud. They show up as video stuttering in "
                 "the back meeting room, as a printer that disappears twice a week, and "
                 "as a till sitting on the guest Wi-Fi because that was convenient at the "
                 "time. Almost always it comes down to the same thing: the network grew "
                 "and was never planned.",

        "leistungen_h": "What €890 includes",
        "leistungen": [
            "Router and switch configured — address ranges, names, fixed addresses for "
            "everything that has to stay reachable",
            "Wi-Fi placed and surveyed: channels, transmit power, hand-over between "
            "access points",
            "Separate networks for the business, guests and equipment — a guest has no "
            "business on the company network, and a till does not belong on guest Wi-Fi",
            "Printers and network drives connected, with fixed addresses",
            "Remote access prepared where it is needed",
            "An overview of what hangs where — with names, addresses and credentials",
        ],
        "nicht_h": "What it does not include",
        "nicht_t": "The devices and the cabling. Pulling cable through an existing "
                   "building is work that cannot be quoted flat — it is added after a "
                   "survey. The same goes for halls, outdoor areas and multiple floors: "
                   "there it becomes surveying and planning, and that stands as its own "
                   "project on the services page.",

        "ablauf_h": "How it works",
        "ablauf": [
            {"h": "Look and measure", "t": "On site: what stands where, where people "
             "work, where the dead spots are today. The measurement decides the number "
             "of access points — nothing is guessed here."},
            {"h": "Setup", "t": "Usually in a day, preferably outside working hours. The "
             "old network stays up until the switch-over."},
            {"h": "Measure again and hand over", "t": "After the build we measure again, "
             "at the same points as before. You get both sets of figures."},
        ],

        "fern_h": "Why guests need a network of their own",
        "fern_t": "A device on the company network can see other devices on the company "
                  "network — that is the point of a network and at the same time its "
                  "risk. A visitor's laptop, a tradesperson's phone or a television in "
                  "the meeting room are devices nobody in the business controls. They "
                  "belong on a network of their own that reaches the internet and nowhere "
                  "else. It costs nothing extra during setup and is hard to retrofit "
                  "later without touching everything.",

        "faq_h": "Common questions",
        "faq": [
            {"q": "Our Wi-Fi is poor in the back room. Would a repeater do?",
             "a": "Rarely. A repeater also repeats a weak signal and halves the speed "
                  "doing it. A second access point on a cable is better — where it "
                  "belongs is decided by the measurement, not by feel."},
            {"q": "Can we keep using our existing equipment?",
             "a": "Often yes. We look at it and say what stays and what should be "
                  "replaced. For consumer-grade equipment replacement usually makes "
                  "sense, because it cannot do separate networks at all."},
            {"q": "How does this differ from the network services page?",
             "a": "This is the setup of a usual office at a fixed price. As soon as "
                  "cabling, halls, outdoor areas or multiple floors are involved it "
                  "becomes a project with planning and surveying — that is on the "
                  "services page and quoted after a survey."},
        ],

        "cta_h": "Ask about a network setup",
        "cta_t": "Tell us briefly how large the area is and how many devices should be "
                 "on the network. Reply within 24 hours.",
        "problem_h": "What is it about?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "firewall-vpn": {
        "titel": "Firewall and VPN setup — €690 fixed price | WVM-IT",
        "desc": "A firewall set up and VPN for access on the move: €690 fixed, with "
                "rules you can still understand later. Get in touch.",
        "h1": "Firewall and VPN — access from outside, without an open door",
        "nav": "Firewall and VPN",
        "kurz": "WVM-IT sets up firewall and VPN for €690: rules on the principle that "
                "whatever is not needed stays closed, VPN access for everyone who works "
                "on the move, and a written overview of which rule exists for what. It "
                "runs remotely as soon as the device is reachable.",
        "intro": "Most firewalls in small businesses are not configured wrongly but not "
                 "configured at all: the provider's router does what it did out of the "
                 "box, and at some point someone set up a forwarding so that accounting "
                 "could work from home. That single forwarding then stays open for years "
                 "— and nobody remembers what it was for.",

        "leistungen_h": "What €690 includes",
        "leistungen": [
            "Firewall configured: closed as the starting point, open only for what is "
            "needed",
            "Existing forwardings cleared up — every one nobody can explain gets closed",
            "VPN for access on the move, set up on computers and phones",
            "Two-factor for the VPN access, where the device supports it",
            "Separate rules for the business, guests and equipment",
            "An overview in plain words: which rule, what for, since when",
        ],
        "nicht_h": "What it does not include",
        "nicht_t": "The device itself. A consumer-grade router cannot do much of this — "
                   "above all no cleanly separated networks and no VPN with two-factor. "
                   "We say beforehand what a suitable device costs; for a small business "
                   "it is usually well below this setup.",

        "ablauf_h": "How it works",
        "ablauf": [
            {"h": "See what is open", "t": "First taking stock: which forwardings exist, "
             "who accesses from outside today, over what. That list almost always "
             "surprises."},
            {"h": "Setup", "t": "The new rules are prepared while the old ones still "
             "apply. The switch happens at an agreed time."},
            {"h": "Hand out access", "t": "Everyone who works on the move gets their own "
             "access — no shared ones. Otherwise nobody knows what to revoke when "
             "someone leaves."},
        ],

        "fern_h": "Why everyone gets their own access",
        "fern_t": "A shared VPN account for everyone is convenient and a problem exactly "
                  "once: on the day someone leaves. The account would then have to be "
                  "changed for everybody, so it is not — and a former employee still "
                  "reaches the company network. With individual accounts, revoking takes "
                  "ten seconds. The same thought lies behind two-factor sign-in: a "
                  "password alone is no longer enough for a door reachable from anywhere "
                  "in the world.",

        "faq_h": "Common questions",
        "faq": [
            {"q": "We already have a firewall in the router.",
             "a": "You do, and it does the bare minimum. The difference is not in its "
                  "existence but in the rules: separate networks, traceable openings and "
                  "a VPN that does not rest on one shared password. Whether your device "
                  "can do that, we check beforehand."},
            {"q": "Will anything get slower?",
             "a": "Not when working on site. Over VPN you notice the route — what comes "
                  "from outside travels through the internet twice. So we set up VPN for "
                  "access to files and programs, not as a permanent line for everything."},
            {"q": "What if we then cannot reach something from outside any more?",
             "a": "That is exactly why taking stock comes first. Whatever is needed today "
                  "stays reachable — just over a route that is known and can be switched "
                  "off. What gets closed is what nobody can explain; and if it later "
                  "turns out it was needed, it is open again in minutes."},
        ],

        "cta_h": "Ask about firewall and VPN",
        "cta_t": "Tell us briefly how many people work on the move and which device is "
                 "in use today. Reply within 24 hours.",
        "problem_h": "What is it about?",
    },

    # ════════════════════════════════════════════════════════════════════════
    "loxone": {
        "titel": "Loxone setup and takeover | WVM-IT",
        "desc": "Taking over, extending or reprogramming an existing Loxone or KNX "
                "system — even when nobody who built it can be reached. Get in touch.",
        "h1": "Loxone setup — even when it is already there",
        "nav": "Taking over Loxone",
        "kurz": "WVM-IT takes over existing Loxone and KNX systems, extends them and "
                "reprograms them: lighting, heating, shading, access control and alarm. "
                "That explicitly includes systems whose installer can no longer be "
                "reached or whose programming nobody knows any more. The price depends "
                "on size and condition and is fixed in writing after a survey.",
        "intro": "Building automation has an awkward property: it works until it does "
                 "not — and then the person who knows why the hall light goes off at ten "
                 "is missing. Houses get sold, electricians close their business, "
                 "programmers cannot be reached. Whoever has inherited a system is not "
                 "looking for someone to build a new one, but for someone who "
                 "understands the existing one.",

        "leistungen_h": "What we do with an existing system",
        "leistungen": [
            "Survey: what is installed, how is it programmed, what no longer works today",
            "Restoring access — even without the installer's documentation",
            "Making the programming readable and documenting it, instead of rebuilding it",
            "Extending: new rooms, new devices, new routines in the same system",
            "Reprogramming when the way the building is used has changed",
            "A briefing, so the system stays operable without us",
            "Connection to the network, safely separated from the rest of the business",
        ],
        "nicht_h": "Why there is no fixed price here",
        "nicht_t": "Because no two systems are alike. A documented Loxone system with "
                   "twenty actuators is something other than a grown KNX installation "
                   "across three floors without any papers. The survey is billed by the "
                   "hour (€120 on site plus travel); after it we quote in writing, and "
                   "then it holds. If it becomes an order, the survey is credited.",

        "ablauf_h": "How it works",
        "ablauf": [
            {"h": "Survey on site", "t": "We look at what is installed and read out the "
             "programming. At the end you know what you have — even if you then decide "
             "against us."},
            {"h": "A quote with numbers", "t": "In writing, separated into takeover, "
             "extension and ongoing support. If we advise against something, it says so."},
            {"h": "Implementation and briefing", "t": "Work happens in stages so the "
             "building stays operable in between. At the end a briefing and the "
             "documentation that was missing before."},
        ],

        "fern_h": "Loxone or KNX — and what if both are installed?",
        "fern_t": "That happens more often than people think: KNX for lighting and "
                  "shading because that is what the electrician worked with, and Loxone "
                  "for everything added later. The two can be connected, and usually that "
                  "is the right route — converting a grown system entirely to one "
                  "platform costs more than it returns. We tell you which parts can stay "
                  "and which are genuinely worth replacing. The general comparison of the "
                  "two systems is in a separate article.",

        "faq_h": "Common questions",
        "faq": [
            {"q": "We have no documentation and no password for the system.",
             "a": "That is the normal case with a takeover. In most cases we reach the "
                  "configuration through the devices themselves. If it really cannot be "
                  "done, we say so after the survey — the question is then which parts "
                  "can be reprogrammed and what has to be replaced."},
            {"q": "Can you extend a system somebody else built?",
             "a": "Yes, that is most of this work. What matters to us is understanding "
                  "the existing logic rather than overwriting it — otherwise neither the "
                  "new nor the old part works afterwards."},
            {"q": "Do you also build new systems?",
             "a": "Yes, together with the electrician and preferably before the first "
                  "cable. That is on the building automation services page, because it is "
                  "a project and not a single task."},
            {"q": "How quickly can you be there when the system is down?",
             "a": "Much can be seen remotely as soon as we have access. If someone has to "
                  "come: in and around the Vöcklabruck district usually the same or the "
                  "next day."},
        ],

        "cta_h": "Ask about a Loxone system",
        "cta_t": "Tell us briefly what is installed and what no longer works. Reply "
                 "within 24 hours.",
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
