from sklearn.metrics import mean_squared_error

def collate_fn(batch):
    input_ids, attention_mask, labels = zip(*batch)

    # Pad sequences to the maximum length in the batch
    input_ids = pad_sequence(input_ids, batch_first=True)
    attention_mask = pad_sequence(attention_mask, batch_first=True)

    return input_ids, attention_mask, torch.stack(labels)


def evaluate_model(model, test_dataloader, criterion, device):
    model.eval()
    all_predictions = []
    all_labels = []
    with torch.no_grad():
        for batch in test_dataloader:
            input_ids, attention_mask, labels = batch
            input_ids, attention_mask, labels = input_ids.to(device), attention_mask.to(device), labels.to(device)

            predictions = model(input_ids, attention_mask)
            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    mse = mean_squared_error(all_labels, all_predictions)
    print(f'Mean Squared Error on Test Set: {mse:.4f}')
    return mse


def predict_model(model, test_dataloader, scaler_likes, device):
    model.eval()
    all_predictions = []
    all_labels = []
    with torch.no_grad():
        for batch in test_dataloader:
            input_ids, attention_mask, labels = batch
            input_ids, attention_mask, labels = input_ids.to(device), attention_mask.to(device), labels.to(device)

            predictions = model(input_ids, attention_mask)
            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    # Convert tensors to NumPy arrays
    y_test_np = np.array(all_labels)
    y_pred_np = np.array(all_predictions)

    # Inverse transform using the scaler
    y_test_inv = scaler_likes.inverse_transform(y_test_np)
    y_pred_inv = scaler_likes.inverse_transform(y_pred_np)

    # Stack the arrays side by side
    comparison_result = np.column_stack((y_test_inv, y_pred_inv))

    # Create a DataFrame for better visualization
    comparison_df = pd.DataFrame(comparison_result, columns=['y_test', 'y_pred'])

    # Display the DataFrame
    comparison_df.to_csv('./ann_results.csv', index=False)

    return comparison_df
