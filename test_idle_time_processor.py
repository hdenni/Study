import unittest
import pandas as pd
import numpy as np
from idle_time_processor import extract_negative_idle_time_rows, create_sample_dataframe


class TestIdleTimeProcessor(unittest.TestCase):
    """Test cases for the idle_time processor functionality."""
    
    def test_basic_functionality(self):
        """Test basic functionality with sample data."""
        df = create_sample_dataframe()
        result = extract_negative_idle_time_rows(df)
        
        # Should extract rows 1,2,3,4,5,6 (indices of negative values and their previous rows)
        expected_indices = [1, 2, 3, 4, 5, 6]
        self.assertEqual(result.index.tolist(), expected_indices)
        
        # Check that negative values are included
        negative_mask = result['idle_time'] < pd.Timedelta(0)
        negative_count = negative_mask.sum()
        self.assertEqual(negative_count, 3)  # rows 2, 4, 6 have negative values
    
    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        empty_df = pd.DataFrame()
        result = extract_negative_idle_time_rows(empty_df)
        self.assertTrue(result.empty)
    
    def test_no_negative_values(self):
        """Test DataFrame with no negative idle_time values."""
        data = {
            'id': [1, 2, 3],
            'idle_time': [
                np.nan,
                pd.Timedelta(seconds=10),
                pd.Timedelta(seconds=5)
            ]
        }
        df = pd.DataFrame(data)
        result = extract_negative_idle_time_rows(df)
        self.assertTrue(result.empty)
    
    def test_only_negative_at_first_row_after_nan(self):
        """Test when the first non-NaN value is negative."""
        data = {
            'id': [1, 2, 3],
            'idle_time': [
                np.nan,
                pd.Timedelta(seconds=-5),  # negative at index 1
                pd.Timedelta(seconds=10)
            ]
        }
        df = pd.DataFrame(data)
        result = extract_negative_idle_time_rows(df)
        
        # Should extract rows 0 and 1 (previous row of negative and the negative row)
        expected_indices = [0, 1]
        self.assertEqual(result.index.tolist(), expected_indices)
    
    def test_all_negative_values(self):
        """Test DataFrame where all non-NaN values are negative."""
        data = {
            'id': [1, 2, 3, 4],
            'idle_time': [
                np.nan,
                pd.Timedelta(seconds=-5),
                pd.Timedelta(seconds=-3),
                pd.Timedelta(seconds=-1)
            ]
        }
        df = pd.DataFrame(data)
        result = extract_negative_idle_time_rows(df)
        
        # Should extract all rows except the first NaN-only row might be included due to being previous
        # Rows 1, 2, 3 are negative, so we get: 0,1 (for row 1), 1,2 (for row 2), 2,3 (for row 3)
        expected_indices = [0, 1, 2, 3]
        self.assertEqual(result.index.tolist(), expected_indices)
    
    def test_single_row_dataframe(self):
        """Test DataFrame with only one row."""
        data = {
            'id': [1],
            'idle_time': [np.nan]
        }
        df = pd.DataFrame(data)
        result = extract_negative_idle_time_rows(df)
        self.assertTrue(result.empty)
    
    def test_two_rows_second_negative(self):
        """Test DataFrame with two rows where second is negative."""
        data = {
            'id': [1, 2],
            'idle_time': [
                np.nan,
                pd.Timedelta(seconds=-5)
            ]
        }
        df = pd.DataFrame(data)
        result = extract_negative_idle_time_rows(df)
        
        # Should extract both rows (row 0 as previous, row 1 as negative)
        expected_indices = [0, 1]
        self.assertEqual(result.index.tolist(), expected_indices)
    
    def test_column_not_found(self):
        """Test error handling when column doesn't exist."""
        df = pd.DataFrame({'other_col': [1, 2, 3]})
        
        with self.assertRaises(ValueError) as context:
            extract_negative_idle_time_rows(df, 'idle_time')
        
        self.assertIn("Column 'idle_time' not found", str(context.exception))
    
    def test_custom_column_name(self):
        """Test with custom column name."""
        data = {
            'id': [1, 2, 3],
            'custom_time': [
                np.nan,
                pd.Timedelta(seconds=10),
                pd.Timedelta(seconds=-5)
            ]
        }
        df = pd.DataFrame(data)
        result = extract_negative_idle_time_rows(df, 'custom_time')
        
        # Should extract rows 1 and 2 (previous and negative)
        expected_indices = [1, 2]
        self.assertEqual(result.index.tolist(), expected_indices)
    
    def test_non_consecutive_negative_values(self):
        """Test with non-consecutive negative values."""
        data = {
            'id': [1, 2, 3, 4, 5, 6],
            'idle_time': [
                np.nan,
                pd.Timedelta(seconds=10),   # positive
                pd.Timedelta(seconds=-5),   # negative (index 2)
                pd.Timedelta(seconds=15),   # positive
                pd.Timedelta(seconds=20),   # positive
                pd.Timedelta(seconds=-3)    # negative (index 5)
            ]
        }
        df = pd.DataFrame(data)
        result = extract_negative_idle_time_rows(df)
        
        # Should extract: 1,2 (for negative at index 2) and 4,5 (for negative at index 5)
        expected_indices = [1, 2, 4, 5]
        self.assertEqual(result.index.tolist(), expected_indices)
    
    def test_preserve_original_dataframe(self):
        """Test that original DataFrame is not modified."""
        original_df = create_sample_dataframe()
        original_copy = original_df.copy()
        
        result = extract_negative_idle_time_rows(original_df)
        
        # Original DataFrame should remain unchanged
        pd.testing.assert_frame_equal(original_df, original_copy)
        
        # Result should be a separate DataFrame
        self.assertIsNot(result, original_df)


if __name__ == '__main__':
    unittest.main(verbosity=2)