import DownloadPayslips
import ParsePDF
import SendOutput


def main():
    print("Welcome to Report Automator!")
    DownloadPayslips.start()
    message = ParsePDF.parse_and_calc()
    SendOutput.send_email("Fortnightly Report", message)


if __name__ == "__main__":
    main()
