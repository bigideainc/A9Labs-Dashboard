import streamlit as st
import pandas as pd

def display_leaderboard():
    st.subheader("Leaderboard")
    
    # Get leaderboard data
    leaderboard_data = st.session_state.data_generator.get_leaderboard_data()
    
    # Create DataFrame
    df = pd.DataFrame(leaderboard_data)
    
    if len(df) == 0:
        st.warning("No validator data available.")
        return
    
    # Convert final_loss to float for proper sorting
    df['final_loss'] = df['final_loss'].astype(float)
    
    # Filtering section
    with st.expander("Filter Options", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            # Miner UID search with case-sensitive option
            search_term = st.text_input(
                "Search Miner UID",
                key="miner_search",
                placeholder="Enter miner UID..."
            )
            case_sensitive = st.checkbox("Case Sensitive Search", value=False)
            
            # Position range filter
            position_range = st.slider(
                "Position Range",
                min_value=1,
                max_value=len(df),
                value=(1, len(df)),
                step=1
            )
        
        with col2:
            # Final loss range
            min_loss = float(df['final_loss'].min())
            max_loss = float(df['final_loss'].max())
            
            loss_range = st.slider(
                "Final Loss Range",
                min_value=min_loss,
                max_value=max_loss,
                value=(min_loss, max_loss),
                step=0.0001,
                format="%.4f"
            )
        
        with col3:
            # Clear filters button
            if st.button("Clear Filters"):
                st.session_state.miner_search = ""
                st.session_state.sort_option = "Position (Default)"
                st.rerun()
    
    # Apply filters
    if search_term:
        if case_sensitive:
            df = df[df['miner_uid'].str.contains(search_term)]
        else:
            df = df[df['miner_uid'].str.contains(search_term, case=False)]
    
    df = df[(df['position'] >= position_range[0]) & (df['position'] <= position_range[1])]
    df = df[(df['final_loss'] >= loss_range[0]) & (df['final_loss'] <= loss_range[1])]
    
    # Sorting options
    col4, col5 = st.columns([3, 1])
    with col4:
        sort_options = {
            "Position (Default)": ("position", True),
            "Position (Reverse)": ("position", False),
            "Miner UID (A-Z)": ("miner_uid", True),
            "Miner UID (Z-A)": ("miner_uid", False),
            "Final Loss (Low to High)": ("final_loss", True),
            "Final Loss (High to Low)": ("final_loss", False)
        }
        
        sort_by = st.selectbox(
            "Sort by",
            options=list(sort_options.keys()),
            key="sort_option"
        )
    
    with col5:
        if len(df) > 0:
            # Export button
            csv = df.to_csv(index=False)
            st.download_button(
                label="Export CSV",
                data=csv,
                file_name="miner_leaderboard.csv",
                mime="text/csv"
            )
    
    # Apply sorting
    sort_column, ascending = sort_options[sort_by]
    df = df.sort_values(sort_column, ascending=ascending)
    
    # Display filtered and sorted dataframe
    if len(df) == 0:
        st.warning("No results found with the current filters.")
    else:
        st.dataframe(
            df,
            hide_index=True,
            column_config={
                "position": st.column_config.NumberColumn(
                    "Position",
                    help="Ranking position",
                    format="%d"
                ),
                "miner_uid": st.column_config.TextColumn(
                    "Miner UID",
                    help="Unique identifier of the miner"
                ),
                "final_loss": st.column_config.NumberColumn(
                    "Final Loss",
                    help="Training loss achieved by the miner",
                    format="%.4f"
                )
            },
            use_container_width=True
        )
        
        # Show stats
        st.caption(f"Showing {len(df)} out of {len(leaderboard_data)} miners")
