from tracker import write_to_md


# Main function
if __name__ == "__main__":
    try:
        write_to_md()
    except Exception:
        print('Error while writing to Markdown')
