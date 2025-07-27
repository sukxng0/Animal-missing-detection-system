def load_labels(label_path):
    with open(label_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    if labels[0] == '???':
        del labels[0]
    return labels
