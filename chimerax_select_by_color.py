import numpy as np

def select_color(session, color_name):
    """
    Select atoms in the current session based on their ChimeraX-defined color.
    
    Parameters:
        session: Current ChimeraX session.
        color_name: Color name as defined in ChimeraX (e.g., "red", "blue").
    """
    from chimerax.core.colors import BuiltinColors
    from chimerax.core.commands import run

    if color_name not in BuiltinColors:
        session.logger.warning(f"Color '{color_name}' not recognized. Use a valid ChimeraX color name.")
        return


    target_color = np.array(BuiltinColors[color_name].rgba, copy=True)
    target_rgb = target_color[:3]
    target_rgb[0]=target_rgb[0]*255
    target_rgb[1]=target_rgb[1]*255
    target_rgb[2]=target_rgb[2]*255

    # Iterate through all models in the session
    selected_residues = []

        
    for model in session.models:
        if not hasattr(model, 'atoms'):
            continue  # Skip models without atoms
        for residue in model.residues:

            res_color = residue.ribbon_color
            res_rgb = res_color[:3]
            if np.allclose(res_rgb, target_rgb):
                selected_residues.append(residue)

        
    # Select matching atoms
    if len(selected_residues)!=0:
        run(session, "select " + " ".join([residue.string(style='command') for residue in selected_residues]))
        session.logger.info(f"Selected {len(selected_residues)} atoms matching color '{color_name}'.")
    else:
        session.logger.warning(f"No atoms found with color '{color_name}'.")


def replace_color(session, color_name, new_color_name):
    select_color(session,color_name)
    from chimerax.core.commands import run
    run(session, f"color sel {new_color_name}")


# Register the script as a command in ChimeraX
from chimerax.core.commands import CmdDesc, register, StringArg
desc = CmdDesc(
    required=[('color_name', StringArg)],
    synopsis='Select atoms based on their visual color in ChimeraX'
)
register('select_color', desc, select_color)
desc2 = CmdDesc(
    required=[('color_name', StringArg),('new_color_name', StringArg)],
    synopsis='Replace color from one to another'
)
register('replace_color', desc2, replace_color)
